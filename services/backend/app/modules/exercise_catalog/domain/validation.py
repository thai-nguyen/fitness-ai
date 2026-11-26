"""Catalog structural validation."""

from __future__ import annotations

from dataclasses import dataclass

from app.modules.exercise_catalog.domain.models import ExerciseCatalog, ExerciseDefinition


@dataclass(frozen=True)
class CatalogIssue:
    code: str
    exercise_id: str | None
    message: str


def validate_exercise(exercise: ExerciseDefinition) -> list[CatalogIssue]:
    issues: list[CatalogIssue] = []
    if not exercise.exercise_id.strip():
        issues.append(CatalogIssue("EMPTY_ID", None, "exercise_id is required"))
    if not exercise.name.strip():
        issues.append(CatalogIssue("EMPTY_NAME", exercise.exercise_id, "name is required"))
    if not exercise.primary_muscle_groups:
        issues.append(
            CatalogIssue(
                "MISSING_PRIMARY_MUSCLE", exercise.exercise_id, "primary_muscle_groups required"
            )
        )
    if not exercise.equipment_requirements:
        issues.append(
            CatalogIssue(
                "MISSING_EQUIPMENT", exercise.exercise_id, "equipment_requirements required"
            )
        )
    if exercise.estimated_duration_seconds <= 0:
        issues.append(
            CatalogIssue(
                "INVALID_DURATION", exercise.exercise_id, "estimated_duration_seconds must be > 0"
            )
        )
    if not exercise.substitution_group.strip():
        issues.append(
            CatalogIssue(
                "MISSING_SUBSTITUTION_GROUP", exercise.exercise_id, "substitution_group required"
            )
        )
    return issues


def validate_catalog(catalog: ExerciseCatalog) -> list[CatalogIssue]:
    issues: list[CatalogIssue] = []
    seen: set[str] = set()
    for exercise in catalog.exercises:
        issues.extend(validate_exercise(exercise))
        if exercise.exercise_id in seen:
            issues.append(
                CatalogIssue(
                    "DUPLICATE_ID", exercise.exercise_id, "duplicate exercise_id in catalog"
                )
            )
        seen.add(exercise.exercise_id)
    return issues
