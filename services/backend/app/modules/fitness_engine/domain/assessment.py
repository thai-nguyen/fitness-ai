"""Fitness assessment input contract and validation."""

from __future__ import annotations

from dataclasses import dataclass

from app.modules.exercise_catalog.domain.models import Equipment
from app.modules.fitness_engine.domain.enums import ExperienceLevel, Goal, Severity, Weekday
from app.modules.fitness_engine.domain.results import ValidationIssue

SUPPORTED_GOALS = frozenset(Goal)
SUPPORTED_EXPERIENCE = frozenset({ExperienceLevel.BEGINNER, ExperienceLevel.INTERMEDIATE})
MIN_SESSION_MINUTES = 20
MAX_SESSION_MINUTES = 90
MIN_TRAINING_DAYS = 1
MAX_TRAINING_DAYS = 5


@dataclass(frozen=True)
class AssessmentInput:
    goal: Goal | None
    experience_level: ExperienceLevel | None
    available_equipment: tuple[Equipment, ...]
    available_training_days: tuple[Weekday, ...]
    preferred_training_days: tuple[Weekday, ...]
    max_session_duration_minutes: int | None
    excluded_exercise_ids: tuple[str, ...] = ()
    known_exercise_restrictions: tuple[str, ...] = ()
    reported_pain_or_safety_concerns: tuple[str, ...] = ()
    adult_eligible: bool | None = None
    assessment_complete: bool = True


def validate_assessment(assessment: AssessmentInput) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    if assessment.goal is None:
        issues.append(
            ValidationIssue(
                code="MISSING_GOAL",
                rule_id="BR-ASSESS-001",
                field="goal",
                severity=Severity.ERROR,
                reason="goal is required",
            )
        )
    elif assessment.goal not in SUPPORTED_GOALS:
        issues.append(
            ValidationIssue(
                code="UNSUPPORTED_GOAL",
                rule_id="BR-ASSESS-002",
                field="goal",
                severity=Severity.ERROR,
                reason=f"unsupported goal: {assessment.goal}",
            )
        )

    if assessment.experience_level is None:
        issues.append(
            ValidationIssue(
                code="MISSING_EXPERIENCE",
                rule_id="BR-ASSESS-001",
                field="experience_level",
                severity=Severity.ERROR,
                reason="experience_level is required",
            )
        )
    elif assessment.experience_level not in SUPPORTED_EXPERIENCE:
        issues.append(
            ValidationIssue(
                code="UNSUPPORTED_EXPERIENCE",
                rule_id="BR-SCOPE-001",
                field="experience_level",
                severity=Severity.ERROR,
                reason="advanced/special populations are out of M04 scope",
            )
        )

    if not assessment.available_equipment:
        issues.append(
            ValidationIssue(
                code="MISSING_EQUIPMENT",
                rule_id="BR-ASSESS-001",
                field="available_equipment",
                severity=Severity.ERROR,
                reason="at least one equipment option is required",
            )
        )

    days = assessment.available_training_days
    if not days:
        issues.append(
            ValidationIssue(
                code="NO_AVAILABLE_DAYS",
                rule_id="BR-SCHED-001",
                field="available_training_days",
                severity=Severity.ERROR,
                reason="at least one available training day is required",
            )
        )
    elif len(days) != len(set(days)):
        issues.append(
            ValidationIssue(
                code="DUPLICATE_DAYS",
                rule_id="BR-SCHED-002",
                field="available_training_days",
                severity=Severity.ERROR,
                reason="available_training_days must be unique",
            )
        )
    elif len(days) > MAX_TRAINING_DAYS:
        issues.append(
            ValidationIssue(
                code="UNSUPPORTED_FREQUENCY",
                rule_id="BR-SCHED-003",
                field="available_training_days",
                severity=Severity.ERROR,
                reason=f"more than {MAX_TRAINING_DAYS} days/week is out of M04 fixture scope",
            )
        )

    preferred = assessment.preferred_training_days
    if preferred:
        if len(preferred) != len(set(preferred)):
            issues.append(
                ValidationIssue(
                    code="DUPLICATE_PREFERRED_DAYS",
                    rule_id="BR-SCHED-002",
                    field="preferred_training_days",
                    severity=Severity.ERROR,
                    reason="preferred_training_days must be unique",
                )
            )
        unavailable = [d for d in preferred if d not in days]
        if unavailable:
            issues.append(
                ValidationIssue(
                    code="PREFERRED_NOT_AVAILABLE",
                    rule_id="BR-SCHED-004",
                    field="preferred_training_days",
                    severity=Severity.ERROR,
                    reason="preferred days must be subset of available days",
                )
            )

    duration = assessment.max_session_duration_minutes
    if duration is None:
        issues.append(
            ValidationIssue(
                code="MISSING_DURATION",
                rule_id="BR-ASSESS-001",
                field="max_session_duration_minutes",
                severity=Severity.ERROR,
                reason="max_session_duration_minutes is required",
            )
        )
    elif duration < MIN_SESSION_MINUTES or duration > MAX_SESSION_MINUTES:
        issues.append(
            ValidationIssue(
                code="INVALID_SESSION_DURATION",
                rule_id="BR-DUR-001",
                field="max_session_duration_minutes",
                severity=Severity.ERROR,
                reason=(
                    f"session duration must be "
                    f"{MIN_SESSION_MINUTES}-{MAX_SESSION_MINUTES} minutes"
                ),
            )
        )

    if assessment.adult_eligible is None:
        issues.append(
            ValidationIssue(
                code="MISSING_ADULT_ELIGIBILITY",
                rule_id="BR-SAFE-001",
                field="adult_eligible",
                severity=Severity.ERROR,
                reason="adult_eligible must be explicitly provided",
            )
        )
    elif assessment.adult_eligible is False:
        issues.append(
            ValidationIssue(
                code="UNSUPPORTED_AGE_ELIGIBILITY",
                rule_id="BR-SCOPE-002",
                field="adult_eligible",
                severity=Severity.ERROR,
                reason="non-adult profiles are unsupported",
            )
        )

    if not assessment.assessment_complete:
        issues.append(
            ValidationIssue(
                code="INCOMPLETE_ASSESSMENT",
                rule_id="BR-ASSESS-003",
                field="assessment_complete",
                severity=Severity.ERROR,
                reason="assessment marked incomplete",
            )
        )

    return issues
