"""Parsing boundary for externally supplied draft mappings (e.g. future LLM JSON).

Typed domain objects remain the trusted in-process representation. This module
rejects missing/invalid schema keys before independent validation.
"""

from __future__ import annotations

from typing import Any

from app.modules.fitness_engine.domain.draft import (
    SCHEMA_VERSION,
    DraftExercise,
    DraftSession,
    IntensityPrescription,
    TrainingPlanDraft,
)
from app.modules.fitness_engine.domain.enums import ExperienceLevel, Goal, Severity, Weekday
from app.modules.fitness_engine.domain.results import ValidationIssue
from app.modules.fitness_engine.domain.rules import RULE_SET_VERSION


class DraftParseError(Exception):
    def __init__(self, issues: list[ValidationIssue]):
        self.issues = issues
        super().__init__("; ".join(i.reason for i in issues))


def _err(code: str, field: str, reason: str) -> ValidationIssue:
    return ValidationIssue(
        code=code,
        rule_id="BR-VAL-001",
        field=field,
        severity=Severity.ERROR,
        reason=reason,
    )


def parse_draft_mapping(data: dict[str, Any]) -> TrainingPlanDraft:
    """Parse a plain dict into TrainingPlanDraft or raise DraftParseError."""
    issues: list[ValidationIssue] = []
    required = (
        "schema_version",
        "rule_set_version",
        "catalog_version",
        "template_id",
        "goal",
        "experience_level",
        "training_days",
        "sessions",
        "warnings",
        "validation_status",
        "review_status",
    )
    for key in required:
        if key not in data:
            issues.append(_err("SCHEMA_MISSING_FIELD", key, f"missing required field {key}"))
    if issues:
        raise DraftParseError(issues)

    try:
        goal = Goal(data["goal"])
        experience = ExperienceLevel(data["experience_level"])
        training_days = tuple(Weekday(d) for d in data["training_days"])
    except (TypeError, ValueError) as exc:
        raise DraftParseError(
            [_err("SCHEMA_ENUM_INVALID", "goal|experience_level|training_days", str(exc))]
        ) from exc

    sessions: list[DraftSession] = []
    try:
        for raw_session in data["sessions"]:
            exercises = []
            for raw_ex in raw_session["exercises"]:
                raw_int = raw_ex["intensity"]
                intensity = IntensityPrescription(
                    repetition_range=tuple(raw_int["repetition_range"]),
                    effort_guidance=str(raw_int["effort_guidance"]),
                    rpe=raw_int.get("rpe"),
                    rest_seconds=int(raw_int["rest_seconds"]),
                    intensity_policy_version=str(raw_int["intensity_policy_version"]),
                )
                exercises.append(
                    DraftExercise(
                        exercise_id=str(raw_ex["exercise_id"]),
                        working_sets=int(raw_ex["working_sets"]),
                        intensity=intensity,
                    )
                )
            sessions.append(
                DraftSession(
                    day=Weekday(raw_session["day"]),
                    estimated_duration_minutes=int(raw_session["estimated_duration_minutes"]),
                    exercises=tuple(exercises),
                )
            )
    except (KeyError, TypeError, ValueError) as exc:
        raise DraftParseError(
            [_err("SCHEMA_SESSION_INVALID", "sessions", f"invalid sessions payload: {exc}")]
        ) from exc

    draft = TrainingPlanDraft(
        schema_version=str(data["schema_version"]),
        rule_set_version=str(data["rule_set_version"]),
        catalog_version=str(data["catalog_version"]),
        template_id=str(data["template_id"]),
        goal=goal,
        experience_level=experience,
        training_days=training_days,
        sessions=tuple(sessions),
        warnings=tuple(data.get("warnings") or ()),
        validation_status=str(data["validation_status"]),
        review_status=str(data["review_status"]),
    )
    # Structural version presence checked; semantic mismatch handled by validate_draft
    _ = SCHEMA_VERSION, RULE_SET_VERSION
    return draft
