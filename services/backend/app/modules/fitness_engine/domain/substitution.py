"""Deterministic exercise substitution for technical drafts."""

from __future__ import annotations

from app.modules.exercise_catalog.domain.models import (
    Equipment,
    ExerciseCatalog,
    ExerciseDefinition,
)
from app.modules.fitness_engine.domain.enums import ExperienceLevel
from app.modules.fitness_engine.domain.results import SubstitutionResult
from app.modules.fitness_engine.domain.selector import SelectionQuery, is_eligible


def find_substitute(
    catalog: ExerciseCatalog,
    original_id: str,
    available_equipment: tuple[Equipment, ...],
    experience: ExperienceLevel,
    excluded_ids: tuple[str, ...] = (),
    restriction_tags: tuple[str, ...] = (),
) -> SubstitutionResult:
    by_id = catalog.by_id()
    original = by_id.get(original_id)
    if original is None:
        return SubstitutionResult(
            original_exercise_id=original_id,
            replacement_exercise_id=None,
            reason="UNKNOWN_ORIGINAL",
            constraints=("original must exist",),
            valid=False,
        )

    excluded = frozenset(excluded_ids) | {original_id}
    query = SelectionQuery(
        movement_pattern=original.movement_pattern,
        available_equipment=frozenset(available_equipment),
        experience=experience,
        excluded_ids=excluded,
        restriction_tags=frozenset(restriction_tags),
    )

    same_group: list[ExerciseDefinition] = []
    other: list[ExerciseDefinition] = []
    for ex in catalog.active():
        if not is_eligible(ex, query):
            continue
        if ex.substitution_group == original.substitution_group:
            same_group.append(ex)
        else:
            other.append(ex)

    candidates = sorted(same_group, key=lambda e: e.exercise_id) or sorted(
        other, key=lambda e: e.exercise_id
    )
    if not candidates:
        return SubstitutionResult(
            original_exercise_id=original_id,
            replacement_exercise_id=None,
            reason="NO_SUBSTITUTE",
            constraints=(
                "movement_pattern",
                "equipment",
                "experience",
                "exclusions",
                "safety_tags",
            ),
            valid=False,
        )

    pick = candidates[0]
    return SubstitutionResult(
        original_exercise_id=original_id,
        replacement_exercise_id=pick.exercise_id,
        reason="SUBSTITUTION_GROUP"
        if pick.substitution_group == original.substitution_group
        else "PATTERN_FALLBACK",
        constraints=(
            "movement_pattern",
            "equipment",
            "experience",
            "exclusions",
            "safety_tags",
            "catalog_eligibility",
        ),
        valid=True,
    )
