"""Minimal intensity policy (provisional; no absolute loads)."""

from __future__ import annotations

from app.modules.fitness_engine.domain.draft import IntensityPrescription
from app.modules.fitness_engine.domain.enums import ExperienceLevel, Goal, Severity
from app.modules.fitness_engine.domain.results import ValidationIssue

INTENSITY_POLICY_VERSION = "m04-intensity-1"


def prescribe_intensity(goal: Goal, experience: ExperienceLevel) -> IntensityPrescription:
    if experience == ExperienceLevel.BEGINNER:
        reps = (8, 12)
        rpe = 6
        rest = 60
        effort = "moderate controlled effort; stop short of failure"
    else:
        if goal == Goal.MUSCLE_GAIN:
            reps = (6, 12)
            rpe = 7
            rest = 90
            effort = "challenging but controlled; leave 2-3 reps in reserve"
        else:
            reps = (8, 15)
            rpe = 7
            rest = 75
            effort = "moderate-hard effort; technical form priority"

    return IntensityPrescription(
        repetition_range=reps,
        effort_guidance=effort,
        rpe=rpe,
        rest_seconds=rest,
        intensity_policy_version=INTENSITY_POLICY_VERSION,
    )


def validate_intensity(
    intensity: IntensityPrescription,
    experience: ExperienceLevel,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    low, high = intensity.repetition_range
    if low < 1 or high > 30 or low > high:
        issues.append(
            ValidationIssue(
                code="INVALID_REPETITION_RANGE",
                rule_id="BR-INT-001",
                field="repetition_range",
                severity=Severity.ERROR,
                reason="repetition_range must satisfy 1 <= low <= high <= 30",
            )
        )
    if intensity.rest_seconds < 0:
        issues.append(
            ValidationIssue(
                code="INVALID_REST",
                rule_id="BR-INT-001",
                field="rest_seconds",
                severity=Severity.ERROR,
                reason="rest_seconds must be >= 0",
            )
        )
    if experience == ExperienceLevel.BEGINNER and intensity.rpe is not None and intensity.rpe > 7:
        issues.append(
            ValidationIssue(
                code="INVALID_INTENSITY",
                rule_id="BR-INT-002",
                field="rpe",
                severity=Severity.ERROR,
                reason="beginner RPE must be null or <= 7",
            )
        )
    if intensity.rpe is not None and (intensity.rpe < 1 or intensity.rpe > 10):
        issues.append(
            ValidationIssue(
                code="INVALID_INTENSITY",
                rule_id="BR-INT-001",
                field="rpe",
                severity=Severity.ERROR,
                reason="rpe must be 1-10 when provided",
            )
        )
    return issues
