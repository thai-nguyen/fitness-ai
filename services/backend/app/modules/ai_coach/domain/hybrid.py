"""Template-first hybrid training personalization (LLM proposes; engine validates)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from typing import Any

from app.modules.ai_coach.domain.prompts import PERSONALIZE, SYS_COACH, load_prompt
from app.modules.ai_coach.providers.contracts import (
    AIMessage,
    AIRole,
    AIStructuredRequest,
)
from app.modules.ai_coach.providers.errors import AIProviderError
from app.modules.exercise_catalog.domain.models import ExerciseCatalog
from app.modules.fitness_engine.domain.assessment import AssessmentInput
from app.modules.fitness_engine.domain.draft import DraftExercise, DraftSession, TrainingPlanDraft
from app.modules.fitness_engine.domain.duration import estimate_minutes
from app.modules.fitness_engine.domain.enums import GenerationOutcome, Severity
from app.modules.fitness_engine.domain.generator import generate_training_plan
from app.modules.fitness_engine.domain.intensity import prescribe_intensity
from app.modules.fitness_engine.domain.results import ValidationIssue
from app.modules.fitness_engine.domain.rules import RULE_SET_VERSION
from app.modules.fitness_engine.domain.selector import SelectionQuery
from app.modules.fitness_engine.domain.templates import TEMPLATES, select_template
from app.modules.fitness_engine.domain.validator import is_technically_validated, validate_draft


class ResponseSource(str, Enum):
    LLM_PERSONALIZED = "LLM_PERSONALIZED"
    LLM_REPAIRED = "LLM_REPAIRED"
    DETERMINISTIC_FALLBACK = "DETERMINISTIC_FALLBACK"
    REJECTED = "REJECTED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"


@dataclass(frozen=True)
class SlotCandidate:
    slot_id: str
    eligible_exercise_ids: tuple[str, ...]


@dataclass(frozen=True)
class HybridResult:
    outcome: GenerationOutcome
    source: ResponseSource
    draft: TrainingPlanDraft | None
    issues: tuple[ValidationIssue, ...]
    proposal: dict[str, Any] | None
    provider_latency_ms: float | None
    repair_attempted: bool


def _eligible_slots(
    assessment: AssessmentInput, catalog: ExerciseCatalog
) -> tuple[Any, tuple[SlotCandidate, ...]] | None:
    prefers_home = True
    prefers_gym = False
    from app.modules.exercise_catalog.domain.models import Equipment

    gym = {Equipment.BARBELL, Equipment.CABLE, Equipment.MACHINE}
    if gym.intersection(assessment.available_equipment):
        prefers_gym = True
        prefers_home = False
    template = select_template(
        assessment.goal,  # type: ignore[arg-type]
        assessment.experience_level,  # type: ignore[arg-type]
        len(assessment.available_training_days),
        prefers_home=prefers_home,
        prefers_gym=prefers_gym,
    )
    if template is None:
        return None
    slots: list[SlotCandidate] = []
    used: set[str] = set()
    for slot in template.slots:
        query = SelectionQuery(
            movement_pattern=slot.movement_pattern,
            available_equipment=frozenset(assessment.available_equipment),
            experience=assessment.experience_level,  # type: ignore[arg-type]
            excluded_ids=frozenset(assessment.excluded_exercise_ids) | used,
            restriction_tags=frozenset(assessment.known_exercise_restrictions),
        )
        from app.modules.fitness_engine.domain.selector import is_eligible

        eligible_ids = [
            e.exercise_id
            for e in sorted(catalog.active(), key=lambda x: x.exercise_id)
            if is_eligible(
                e,
                SelectionQuery(
                    movement_pattern=slot.movement_pattern,
                    available_equipment=query.available_equipment,
                    experience=query.experience,
                    excluded_ids=frozenset(assessment.excluded_exercise_ids) | used,
                    restriction_tags=query.restriction_tags,
                ),
            )
        ]
        if not eligible_ids and slot.required:
            return None
        if eligible_ids:
            slots.append(SlotCandidate(slot.slot_id, tuple(eligible_ids[:5])))
            used.add(eligible_ids[0])
    return template, tuple(slots)


def _build_draft_from_choices(
    assessment: AssessmentInput,
    catalog: ExerciseCatalog,
    template_id: str,
    choices: dict[str, str],
    baseline_days,
) -> TrainingPlanDraft | None:
    template = next((t for t in TEMPLATES if t.template_id == template_id), None)
    if template is None:
        return None
    intensity = prescribe_intensity(assessment.goal, assessment.experience_level)  # type: ignore[arg-type]
    selected = []
    for slot in template.slots:
        eid = choices.get(slot.slot_id)
        if eid is None:
            if slot.required:
                return None
            continue
        ex = catalog.by_id().get(eid)
        if ex is None:
            return None
        selected.append((ex, template.default_working_sets, intensity))
    if not selected:
        return None
    minutes = estimate_minutes(selected)
    exercises = tuple(
        DraftExercise(ex.exercise_id, sets, intensity) for ex, sets, intensity in selected
    )
    sessions = tuple(
        DraftSession(day=d, estimated_duration_minutes=minutes, exercises=exercises)
        for d in baseline_days
    )
    from app.modules.fitness_engine.domain.draft import SCHEMA_VERSION

    return TrainingPlanDraft(
        schema_version=SCHEMA_VERSION,
        rule_set_version=RULE_SET_VERSION,
        catalog_version=catalog.catalog_version,
        template_id=template_id,
        goal=assessment.goal,  # type: ignore[arg-type]
        experience_level=assessment.experience_level,  # type: ignore[arg-type]
        training_days=baseline_days,
        sessions=sessions,
        warnings=(),
        validation_status="PENDING",
        review_status="TECHNICAL_DRAFT_ONLY",
    )


def _parse_proposal(text: str) -> dict[str, Any]:
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("proposal must be object")
    return data


async def hybrid_generate(
    assessment: AssessmentInput,
    catalog: ExerciseCatalog,
    provider,
    *,
    max_repair: int = 1,
    temperature: float = 0.2,
    max_tokens: int = 1024,
) -> HybridResult:
    """Strategy C: deterministic candidates + LLM personalization + independent validate."""
    baseline = generate_training_plan(assessment, catalog)
    if baseline.outcome != GenerationOutcome.VALIDATED_TECHNICAL_DRAFT:
        source = (
            ResponseSource.REVIEW_REQUIRED
            if baseline.outcome == GenerationOutcome.REVIEW_REQUIRED
            else ResponseSource.REJECTED
        )
        return HybridResult(
            outcome=baseline.outcome,
            source=source,
            draft=None,
            issues=baseline.issues,
            proposal=None,
            provider_latency_ms=None,
            repair_attempted=False,
        )

    packed = _eligible_slots(assessment, catalog)
    if packed is None:
        return HybridResult(
            outcome=GenerationOutcome.INSUFFICIENT_CATALOG,
            source=ResponseSource.REJECTED,
            draft=None,
            issues=(),
            proposal=None,
            provider_latency_ms=None,
            repair_attempted=False,
        )
    template, slots = packed
    assert baseline.draft is not None

    payload = {
        "template_id": template.template_id,
        "slots": [
            {"slot_id": s.slot_id, "eligible_exercise_ids": list(s.eligible_exercise_ids)}
            for s in slots
        ],
        "goal": assessment.goal.value if assessment.goal else None,
        "experience_level": (
            assessment.experience_level.value if assessment.experience_level else None
        ),
    }
    messages = (
        AIMessage(AIRole.SYSTEM, load_prompt(SYS_COACH)),
        AIMessage(AIRole.USER, load_prompt(PERSONALIZE) + "\n\n" + json.dumps(payload)),
    )
    req = AIStructuredRequest(
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        force_json=True,
        request_id="hybrid-personalize",
    )

    repair_attempted = False
    provider_latency = None
    last_issues: list[ValidationIssue] = []
    proposal = None

    for attempt in range(max_repair + 1):
        try:
            if attempt > 0:
                repair_attempted = True
                err_msg = json.dumps(
                    [
                        {"code": i.code, "rule_id": i.rule_id, "reason": i.reason}
                        for i in last_issues
                    ]
                )
                messages = (
                    messages[0],
                    AIMessage(
                        AIRole.USER,
                        "Repair the JSON proposal. Errors:\n"
                        + err_msg
                        + "\nCandidates:\n"
                        + json.dumps(payload),
                    ),
                )
                req = AIStructuredRequest(
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    force_json=True,
                    request_id=f"hybrid-repair-{attempt}",
                )
            resp = await provider.structured(req)
            provider_latency = resp.latency_ms
            proposal = _parse_proposal(resp.text)
        except (AIProviderError, json.JSONDecodeError, ValueError, TypeError) as exc:
            last_issues = [
                ValidationIssue(
                    code="LLM_STRUCTURED_FAILURE",
                    rule_id="BR-VAL-001",
                    field="proposal",
                    severity=Severity.ERROR,
                    reason=str(getattr(exc, "message", exc))[:200],
                )
            ]
            continue

        template_id = proposal.get("template_id") or template.template_id
        choices_list = proposal.get("exercise_choices") or []
        choices = {
            c.get("slot_id"): c.get("exercise_id")
            for c in choices_list
            if isinstance(c, dict) and c.get("slot_id") and c.get("exercise_id")
        }
        # enforce allowlist
        allow = {s.slot_id: set(s.eligible_exercise_ids) for s in slots}
        for slot_id, eid in list(choices.items()):
            if slot_id not in allow or eid not in allow[slot_id]:
                last_issues = [
                    ValidationIssue(
                        code="INVALID_CANDIDATE_REFERENCE",
                        rule_id="BR-VAL-001",
                        field="exercise_choices",
                        severity=Severity.ERROR,
                        reason=f"exercise {eid} not eligible for {slot_id}",
                        entity_id=str(eid),
                    )
                ]
                choices = {}
                break
        if not choices:
            continue

        draft = _build_draft_from_choices(
            assessment, catalog, template_id, choices, baseline.draft.training_days
        )
        if draft is None:
            last_issues = [
                ValidationIssue(
                    code="DRAFT_BUILD_FAILED",
                    rule_id="BR-VAL-001",
                    field="proposal",
                    severity=Severity.ERROR,
                    reason="could not build draft from proposal",
                )
            ]
            continue
        issues = validate_draft(draft, catalog, assessment)
        if is_technically_validated(issues):
            validated = TrainingPlanDraft(
                schema_version=draft.schema_version,
                rule_set_version=draft.rule_set_version,
                catalog_version=draft.catalog_version,
                template_id=draft.template_id,
                goal=draft.goal,
                experience_level=draft.experience_level,
                training_days=draft.training_days,
                sessions=draft.sessions,
                warnings=tuple(i.reason for i in issues if i.severity == Severity.WARNING),
                validation_status="VALIDATED_TECHNICAL_DRAFT",
                review_status="TECHNICAL_DRAFT_ONLY",
            )
            return HybridResult(
                outcome=GenerationOutcome.VALIDATED_TECHNICAL_DRAFT,
                source=(
                    ResponseSource.LLM_REPAIRED
                    if repair_attempted
                    else ResponseSource.LLM_PERSONALIZED
                ),
                draft=validated,
                issues=(),
                proposal=proposal,
                provider_latency_ms=provider_latency,
                repair_attempted=repair_attempted,
            )
        last_issues = [i for i in issues if i.severity == Severity.ERROR]

    # Deterministic fallback — must still validate
    return HybridResult(
        outcome=GenerationOutcome.VALIDATED_TECHNICAL_DRAFT,
        source=ResponseSource.DETERMINISTIC_FALLBACK,
        draft=baseline.draft,
        issues=tuple(last_issues),
        proposal=proposal,
        provider_latency_ms=provider_latency,
        repair_attempted=repair_attempted,
    )
