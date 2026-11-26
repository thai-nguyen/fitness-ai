"""Deterministic exercise selection."""

from __future__ import annotations

from dataclasses import dataclass

from app.modules.exercise_catalog.domain.models import (
    Difficulty,
    Equipment,
    ExerciseCatalog,
    ExerciseDefinition,
    MovementPattern,
)
from app.modules.fitness_engine.domain.enums import ExperienceLevel


@dataclass(frozen=True)
class SelectionQuery:
    movement_pattern: MovementPattern
    available_equipment: frozenset[Equipment]
    experience: ExperienceLevel
    excluded_ids: frozenset[str]
    restriction_tags: frozenset[str]


@dataclass(frozen=True)
class SelectionResult:
    exercise: ExerciseDefinition | None
    reason: str


def difficulty_allowed(experience: ExperienceLevel, difficulty: Difficulty) -> bool:
    if experience == ExperienceLevel.BEGINNER:
        return difficulty == Difficulty.BEGINNER
    if experience == ExperienceLevel.INTERMEDIATE:
        return difficulty in {Difficulty.BEGINNER, Difficulty.INTERMEDIATE}
    return False


def is_eligible(exercise: ExerciseDefinition, query: SelectionQuery) -> bool:
    if not exercise.active_status:
        return False
    if exercise.exercise_id in query.excluded_ids:
        return False
    if exercise.movement_pattern != query.movement_pattern:
        return False
    if not set(exercise.equipment_requirements).issubset(query.available_equipment):
        return False
    if not difficulty_allowed(query.experience, exercise.difficulty):
        return False
    if query.restriction_tags.intersection(exercise.contraindication_tags):
        return False
    return True


def select_exercise(catalog: ExerciseCatalog, query: SelectionQuery) -> SelectionResult:
    eligible = [e for e in catalog.active() if is_eligible(e, query)]
    if not eligible:
        return SelectionResult(None, "INSUFFICIENT_CATALOG")
    # Stable tie-break: exercise_id ascending
    eligible.sort(key=lambda e: e.exercise_id)
    return SelectionResult(eligible[0], "SELECTED")


def select_for_slots(
    catalog: ExerciseCatalog,
    slots: tuple,
    available_equipment: tuple[Equipment, ...],
    experience: ExperienceLevel,
    excluded_ids: tuple[str, ...],
    restriction_tags: tuple[str, ...],
) -> tuple[list[ExerciseDefinition], str | None]:
    used: set[str] = set()
    selected: list[ExerciseDefinition] = []
    equipment = frozenset(available_equipment)
    excluded = frozenset(excluded_ids)
    restrictions = frozenset(restriction_tags)

    for slot in slots:
        query = SelectionQuery(
            movement_pattern=slot.movement_pattern,
            available_equipment=equipment,
            experience=experience,
            excluded_ids=excluded | used,
            restriction_tags=restrictions,
        )
        result = select_exercise(catalog, query)
        if result.exercise is None:
            if slot.required:
                return [], "INSUFFICIENT_CATALOG"
            continue
        selected.append(result.exercise)
        used.add(result.exercise.exercise_id)
    return selected, None
