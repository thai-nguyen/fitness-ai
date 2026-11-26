"""Independent training plan draft validator.

Does not assume the draft was produced by the generator. Recalculates duration
from the exercise prescription; does not trust declared estimated_duration alone.
"""

from __future__ import annotations

from app.modules.exercise_catalog.domain.models import ExerciseCatalog, ExerciseDefinition
from app.modules.fitness_engine.domain.assessment import AssessmentInput
from app.modules.fitness_engine.domain.draft import (
    SCHEMA_VERSION,
    DraftSession,
    IntensityPrescription,
    TrainingPlanDraft,
)
from app.modules.fitness_engine.domain.duration import estimate_minutes
from app.modules.fitness_engine.domain.enums import Severity
from app.modules.fitness_engine.domain.intensity import validate_intensity
from app.modules.fitness_engine.domain.results import ValidationIssue
from app.modules.fitness_engine.domain.rules import RULE_SET_VERSION
from app.modules.fitness_engine.domain.selector import difficulty_allowed
from app.modules.fitness_engine.domain.templates import TEMPLATES
from app.modules.fitness_engine.domain.volume import volume_issues

# Declared duration may differ from recalculated by at most this tolerance (minutes).
DECLARED_DURATION_TOLERANCE_MINUTES = 0


def _templates_by_id() -> dict[str, object]:
    return {t.template_id: t for t in TEMPLATES}


def _recalculated_session_minutes(
    session: DraftSession,
    by_id: dict[str, ExerciseDefinition],
) -> int | None:
    """Return estimated minutes from prescription, or None if any exercise is unknown."""
    pairs: list[tuple[ExerciseDefinition, int, IntensityPrescription]] = []
    for item in session.exercises:
        ex = by_id.get(item.exercise_id)
        if ex is None:
            return None
        pairs.append((ex, item.working_sets, item.intensity))
    if not pairs:
        return 0
    return estimate_minutes(pairs)


def validate_draft(
    draft: TrainingPlanDraft,
    catalog: ExerciseCatalog,
    assessment: AssessmentInput | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    by_id = catalog.by_id()
    templates = _templates_by_id()

    if draft.schema_version != SCHEMA_VERSION:
        issues.append(
            ValidationIssue(
                code="SCHEMA_MISMATCH",
                rule_id="BR-VAL-001",
                field="schema_version",
                severity=Severity.ERROR,
                reason=f"unsupported schema_version {draft.schema_version}",
            )
        )
    if draft.rule_set_version != RULE_SET_VERSION:
        issues.append(
            ValidationIssue(
                code="RULE_VERSION_MISMATCH",
                rule_id="BR-VAL-001",
                field="rule_set_version",
                severity=Severity.ERROR,
                reason=f"unsupported rule_set_version {draft.rule_set_version}",
            )
        )
    if draft.catalog_version != catalog.catalog_version:
        issues.append(
            ValidationIssue(
                code="CATALOG_VERSION_MISMATCH",
                rule_id="BR-VAL-001",
                field="catalog_version",
                severity=Severity.ERROR,
                reason="draft catalog_version does not match provided catalog",
            )
        )

    template = templates.get(draft.template_id)
    if template is None:
        issues.append(
            ValidationIssue(
                code="UNKNOWN_TEMPLATE",
                rule_id="BR-VAL-001",
                field="template_id",
                severity=Severity.ERROR,
                reason=f"unknown template_id {draft.template_id}",
            )
        )
    else:
        if draft.goal not in template.supported_goals:
            issues.append(
                ValidationIssue(
                    code="TEMPLATE_GOAL_INCOMPATIBLE",
                    rule_id="BR-ASSESS-002",
                    field="template_id",
                    severity=Severity.ERROR,
                    reason="template does not support draft goal",
                    entity_id=draft.template_id,
                )
            )
        if draft.experience_level not in template.supported_experience:
            issues.append(
                ValidationIssue(
                    code="TEMPLATE_EXPERIENCE_INCOMPATIBLE",
                    rule_id="BR-SCOPE-001",
                    field="template_id",
                    severity=Severity.ERROR,
                    reason="template does not support draft experience_level",
                    entity_id=draft.template_id,
                )
            )
        if assessment and len(assessment.available_training_days) < template.min_days:
            issues.append(
                ValidationIssue(
                    code="TEMPLATE_SCHEDULE_INFEASIBLE",
                    rule_id="BR-SCHED-003",
                    field="available_training_days",
                    severity=Severity.ERROR,
                    reason="available days below template minimum",
                    entity_id=draft.template_id,
                )
            )

    if not draft.sessions:
        issues.append(
            ValidationIssue(
                code="MISSING_SESSIONS",
                rule_id="BR-VAL-001",
                field="sessions",
                severity=Severity.ERROR,
                reason="draft must include at least one session",
            )
        )

    seen_days: set = set()
    for session in draft.sessions:
        if session.day in seen_days:
            issues.append(
                ValidationIssue(
                    code="DUPLICATE_SESSION_DAY",
                    rule_id="BR-SCHED-002",
                    field="sessions.day",
                    severity=Severity.ERROR,
                    reason=f"duplicate session day {session.day.value}",
                    entity_id=session.day.value,
                )
            )
        seen_days.add(session.day)

        if assessment and session.day not in assessment.available_training_days:
            issues.append(
                ValidationIssue(
                    code="SCHEDULE_OUTSIDE_AVAILABILITY",
                    rule_id="BR-SCHED-001",
                    field="sessions.day",
                    severity=Severity.ERROR,
                    reason="session scheduled outside available days",
                    entity_id=session.day.value,
                )
            )

        if session.estimated_duration_minutes < 0:
            issues.append(
                ValidationIssue(
                    code="INVALID_DECLARED_DURATION",
                    rule_id="BR-DUR-001",
                    field="estimated_duration_minutes",
                    severity=Severity.ERROR,
                    reason="estimated_duration_minutes must be >= 0",
                    entity_id=session.day.value,
                )
            )

        recalculated = _recalculated_session_minutes(session, by_id)
        if recalculated is not None:
            if abs(session.estimated_duration_minutes - recalculated) > (
                DECLARED_DURATION_TOLERANCE_MINUTES
            ):
                issues.append(
                    ValidationIssue(
                        code="DECLARED_DURATION_MISMATCH",
                        rule_id="BR-DUR-002",
                        field="estimated_duration_minutes",
                        severity=Severity.ERROR,
                        reason=(
                            f"declared duration {session.estimated_duration_minutes} "
                            f"!= recalculated {recalculated} from prescription"
                        ),
                        entity_id=session.day.value,
                    )
                )
            effective_minutes = recalculated
        else:
            # Unknown IDs already flagged; still apply declared vs max as fail-closed signal
            effective_minutes = session.estimated_duration_minutes

        if assessment and assessment.max_session_duration_minutes is not None:
            if effective_minutes > assessment.max_session_duration_minutes:
                issues.append(
                    ValidationIssue(
                        code="SESSION_DURATION_VIOLATION",
                        rule_id="BR-DUR-002",
                        field="estimated_duration_minutes",
                        severity=Severity.ERROR,
                        reason="session duration exceeds max_session_duration_minutes",
                        entity_id=session.day.value,
                    )
                )

        session_ids: set[str] = set()
        for item in session.exercises:
            if item.exercise_id in session_ids:
                issues.append(
                    ValidationIssue(
                        code="DUPLICATE_EXERCISE",
                        rule_id="BR-VAL-001",
                        field="exercises.exercise_id",
                        severity=Severity.ERROR,
                        reason="duplicate exercise in session",
                        entity_id=item.exercise_id,
                    )
                )
            session_ids.add(item.exercise_id)

            ex = by_id.get(item.exercise_id)
            if ex is None:
                issues.append(
                    ValidationIssue(
                        code="UNKNOWN_EXERCISE_ID",
                        rule_id="BR-VAL-001",
                        field="exercises.exercise_id",
                        severity=Severity.ERROR,
                        reason="exercise_id not in catalog",
                        entity_id=item.exercise_id,
                    )
                )
                continue

            if not ex.active_status:
                issues.append(
                    ValidationIssue(
                        code="INACTIVE_EXERCISE",
                        rule_id="BR-SEL-002",
                        field="exercises.exercise_id",
                        severity=Severity.ERROR,
                        reason="inactive exercise in draft",
                        entity_id=item.exercise_id,
                    )
                )

            if not difficulty_allowed(draft.experience_level, ex.difficulty):
                issues.append(
                    ValidationIssue(
                        code="EXPERIENCE_DIFFICULTY_INCOMPATIBLE",
                        rule_id="BR-SEL-003",
                        field="experience_level",
                        severity=Severity.ERROR,
                        reason="exercise difficulty exceeds draft experience policy",
                        entity_id=item.exercise_id,
                    )
                )

            if assessment:
                available = frozenset(assessment.available_equipment)
                if not set(ex.equipment_requirements).issubset(available):
                    issues.append(
                        ValidationIssue(
                            code="EQUIPMENT_INCOMPATIBLE",
                            rule_id="BR-SEL-001",
                            field="equipment_requirements",
                            severity=Severity.ERROR,
                            reason="exercise equipment not available",
                            entity_id=item.exercise_id,
                        )
                    )
                if item.exercise_id in assessment.excluded_exercise_ids:
                    issues.append(
                        ValidationIssue(
                            code="EXCLUDED_EXERCISE",
                            rule_id="BR-SEL-004",
                            field="excluded_exercise_ids",
                            severity=Severity.ERROR,
                            reason="excluded exercise present in draft",
                            entity_id=item.exercise_id,
                        )
                    )
                restriction = frozenset(assessment.known_exercise_restrictions)
                if restriction.intersection(ex.contraindication_tags):
                    issues.append(
                        ValidationIssue(
                            code="SAFETY_RESTRICTION",
                            rule_id="BR-SEL-004",
                            field="known_exercise_restrictions",
                            severity=Severity.ERROR,
                            reason="exercise hits known restriction tags",
                            entity_id=item.exercise_id,
                        )
                    )

            issues.extend(validate_intensity(item.intensity, draft.experience_level))

    issues.extend(volume_issues(draft, catalog))
    return issues


def is_technically_validated(issues: list[ValidationIssue]) -> bool:
    return not any(i.severity == Severity.ERROR for i in issues)
