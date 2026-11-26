"""Deterministic training plan generation pipeline (no LLM)."""

from __future__ import annotations

from app.modules.exercise_catalog.domain.models import Equipment, ExerciseCatalog
from app.modules.fitness_engine.domain.assessment import AssessmentInput, validate_assessment
from app.modules.fitness_engine.domain.draft import (
    SCHEMA_VERSION,
    DraftExercise,
    DraftSession,
    TrainingPlanDraft,
)
from app.modules.fitness_engine.domain.duration import estimate_minutes, fits_duration
from app.modules.fitness_engine.domain.enums import (
    GenerationOutcome,
    SafetyOutcome,
    Severity,
)
from app.modules.fitness_engine.domain.intensity import prescribe_intensity
from app.modules.fitness_engine.domain.results import GenerationResult, ValidationIssue
from app.modules.fitness_engine.domain.rules import RULE_SET_VERSION
from app.modules.fitness_engine.domain.safety import screen_safety
from app.modules.fitness_engine.domain.schedule import allocate_schedule
from app.modules.fitness_engine.domain.selector import select_for_slots
from app.modules.fitness_engine.domain.templates import TrainingTemplate, select_template
from app.modules.fitness_engine.domain.validator import is_technically_validated, validate_draft


def _prefers_home(equipment: tuple[Equipment, ...]) -> bool:
    gym_markers = {Equipment.BARBELL, Equipment.CABLE, Equipment.MACHINE, Equipment.BENCH}
    return not gym_markers.intersection(equipment)


def _prefers_gym(equipment: tuple[Equipment, ...]) -> bool:
    gym_markers = {Equipment.BARBELL, Equipment.CABLE, Equipment.MACHINE}
    return bool(gym_markers.intersection(equipment))


def _build_session_exercises(
    selected,
    working_sets: int,
    intensity,
):
    return [
        DraftExercise(exercise_id=ex.exercise_id, working_sets=working_sets, intensity=intensity)
        for ex in selected
    ]


def _try_build_draft(
    assessment: AssessmentInput,
    catalog: ExerciseCatalog,
    template: TrainingTemplate,
    days,
    drop_optional: bool,
) -> tuple[TrainingPlanDraft | None, list[ValidationIssue], str | None]:
    slots = template.slots if not drop_optional else tuple(s for s in template.slots if s.required)
    selected, sel_err = select_for_slots(
        catalog,
        slots,
        assessment.available_equipment,
        assessment.experience_level,  # type: ignore[arg-type]
        assessment.excluded_exercise_ids,
        assessment.known_exercise_restrictions,
    )
    if sel_err:
        return None, [], sel_err

    intensity = prescribe_intensity(assessment.goal, assessment.experience_level)  # type: ignore[arg-type]
    working_sets = template.default_working_sets
    # Duration feasibility: optionally reduce sets once
    pairs = [(ex, working_sets, intensity) for ex in selected]
    estimated = estimate_minutes(pairs)
    max_minutes = assessment.max_session_duration_minutes or 0
    if not fits_duration(estimated, max_minutes) and working_sets > 1:
        working_sets -= 1
        pairs = [(ex, working_sets, intensity) for ex in selected]
        estimated = estimate_minutes(pairs)
    if not fits_duration(estimated, max_minutes):
        return (
            None,
            [
                ValidationIssue(
                    code="SESSION_DURATION_VIOLATION",
                    rule_id="BR-DUR-002",
                    field="max_session_duration_minutes",
                    severity=Severity.ERROR,
                    reason="estimated session duration exceeds available time",
                )
            ],
            "INFEASIBLE_CONSTRAINTS",
        )

    draft_exercises = _build_session_exercises(selected, working_sets, intensity)
    sessions = tuple(
        DraftSession(
            day=day, estimated_duration_minutes=estimated, exercises=tuple(draft_exercises)
        )
        for day in days
    )
    draft = TrainingPlanDraft(
        schema_version=SCHEMA_VERSION,
        rule_set_version=RULE_SET_VERSION,
        catalog_version=catalog.catalog_version,
        template_id=template.template_id,
        goal=assessment.goal,  # type: ignore[arg-type]
        experience_level=assessment.experience_level,  # type: ignore[arg-type]
        training_days=days,
        sessions=sessions,
        warnings=(),
        validation_status="PENDING",
        review_status="TECHNICAL_DRAFT_ONLY",
    )
    return draft, [], None


def generate_training_plan(
    assessment: AssessmentInput,
    catalog: ExerciseCatalog,
) -> GenerationResult:
    """Full pipeline: validate → safety → template → schedule → select → draft → validate."""

    input_issues = validate_assessment(assessment)
    hard_input = [i for i in input_issues if i.severity == Severity.ERROR]
    if hard_input:
        unsupported_codes = {
            "UNSUPPORTED_GOAL",
            "UNSUPPORTED_EXPERIENCE",
            "UNSUPPORTED_AGE_ELIGIBILITY",
            "UNSUPPORTED_FREQUENCY",
        }
        if any(i.code in unsupported_codes for i in hard_input):
            outcome = GenerationOutcome.UNSUPPORTED_PROFILE
        else:
            outcome = GenerationOutcome.INVALID_INPUT
        return GenerationResult(outcome=outcome, draft=None, issues=tuple(hard_input), safety=None)

    safety = screen_safety(assessment)
    if safety.outcome == SafetyOutcome.REVIEW_REQUIRED:
        return GenerationResult(
            outcome=GenerationOutcome.REVIEW_REQUIRED,
            draft=None,
            issues=safety.issues,
            safety=safety,
        )
    if safety.outcome == SafetyOutcome.INSUFFICIENT_INFORMATION:
        return GenerationResult(
            outcome=GenerationOutcome.INVALID_INPUT,
            draft=None,
            issues=safety.issues,
            safety=safety,
        )
    if safety.outcome == SafetyOutcome.REJECTED:
        return GenerationResult(
            outcome=GenerationOutcome.UNSUPPORTED_PROFILE,
            draft=None,
            issues=safety.issues,
            safety=safety,
        )

    prefers_home = _prefers_home(assessment.available_equipment)
    prefers_gym = _prefers_gym(assessment.available_equipment)
    template = select_template(
        assessment.goal,  # type: ignore[arg-type]
        assessment.experience_level,  # type: ignore[arg-type]
        len(assessment.available_training_days),
        prefers_home=prefers_home,
        prefers_gym=prefers_gym,
    )
    if template is None:
        return GenerationResult(
            outcome=GenerationOutcome.INFEASIBLE_CONSTRAINTS,
            draft=None,
            issues=(
                ValidationIssue(
                    code="NO_COMPATIBLE_TEMPLATE",
                    rule_id="BR-ASSESS-002",
                    field="goal",
                    severity=Severity.ERROR,
                    reason="no compatible provisional template",
                ),
            ),
            safety=safety,
        )

    schedule = allocate_schedule(
        assessment.available_training_days,
        assessment.preferred_training_days,
        template,
    )
    if schedule.days is None:
        return GenerationResult(
            outcome=GenerationOutcome.INFEASIBLE_CONSTRAINTS,
            draft=None,
            issues=schedule.issues,
            safety=safety,
        )

    # Attempt with optional slots, then without if duration/catalog fails
    draft, pre_issues, err = _try_build_draft(
        assessment, catalog, template, schedule.days, drop_optional=False
    )
    if err == "INSUFFICIENT_CATALOG":
        draft, pre_issues, err = _try_build_draft(
            assessment, catalog, template, schedule.days, drop_optional=True
        )
    if err == "INSUFFICIENT_CATALOG":
        return GenerationResult(
            outcome=GenerationOutcome.INSUFFICIENT_CATALOG,
            draft=None,
            issues=(
                ValidationIssue(
                    code="INSUFFICIENT_CATALOG",
                    rule_id="BR-SEL-001",
                    field="catalog",
                    severity=Severity.ERROR,
                    reason="no eligible exercises for required template slots",
                ),
            ),
            safety=safety,
        )
    if err == "INFEASIBLE_CONSTRAINTS":
        # Try dropping optional components
        draft2, pre_issues2, err2 = _try_build_draft(
            assessment, catalog, template, schedule.days, drop_optional=True
        )
        if err2:
            return GenerationResult(
                outcome=GenerationOutcome.INFEASIBLE_CONSTRAINTS,
                draft=None,
                issues=tuple(pre_issues or pre_issues2),
                safety=safety,
            )
        draft, pre_issues = draft2, pre_issues2

    assert draft is not None
    validation_issues = validate_draft(draft, catalog, assessment)
    warnings = tuple(i for i in validation_issues if i.severity == Severity.WARNING)
    errors = [i for i in validation_issues if i.severity == Severity.ERROR]
    if not is_technically_validated(validation_issues):
        return GenerationResult(
            outcome=GenerationOutcome.VALIDATION_FAILED,
            draft=None,
            issues=tuple(errors),
            safety=safety,
            warnings=warnings,
        )

    validated = TrainingPlanDraft(
        schema_version=draft.schema_version,
        rule_set_version=draft.rule_set_version,
        catalog_version=draft.catalog_version,
        template_id=draft.template_id,
        goal=draft.goal,
        experience_level=draft.experience_level,
        training_days=draft.training_days,
        sessions=draft.sessions,
        warnings=tuple(w.reason for w in warnings),
        validation_status="VALIDATED_TECHNICAL_DRAFT",
        review_status="TECHNICAL_DRAFT_ONLY",
    )
    return GenerationResult(
        outcome=GenerationOutcome.VALIDATED_TECHNICAL_DRAFT,
        draft=validated,
        issues=(),
        safety=safety,
        warnings=warnings,
    )
