"""Helpers for constructing drafts with recalculated durations."""

from __future__ import annotations

from app.modules.exercise_catalog.domain.models import ExerciseCatalog
from app.modules.fitness_engine.domain.draft import (
    SCHEMA_VERSION,
    DraftExercise,
    DraftSession,
    IntensityPrescription,
    TrainingPlanDraft,
)
from app.modules.fitness_engine.domain.duration import estimate_minutes
from app.modules.fitness_engine.domain.enums import ExperienceLevel, Goal, Weekday
from app.modules.fitness_engine.domain.intensity import prescribe_intensity


def session_with_exercises(
    catalog: ExerciseCatalog,
    day: Weekday,
    items: list[tuple[str, int, IntensityPrescription]],
    *,
    declared_minutes: int | None = None,
) -> DraftSession:
    pairs = []
    draft_items = []
    for exercise_id, sets, intensity in items:
        ex = catalog.by_id()[exercise_id]
        pairs.append((ex, sets, intensity))
        draft_items.append(DraftExercise(exercise_id, sets, intensity))
    minutes = declared_minutes if declared_minutes is not None else estimate_minutes(pairs)
    return DraftSession(day=day, estimated_duration_minutes=minutes, exercises=tuple(draft_items))


def make_draft(
    catalog: ExerciseCatalog,
    *,
    exercise_id: str = "ex_bw_squat",
    working_sets: int = 2,
    intensity: IntensityPrescription | None = None,
    day: Weekday = Weekday.MON,
    experience: ExperienceLevel = ExperienceLevel.BEGINNER,
    goal: Goal = Goal.GENERAL_FITNESS,
    template_id: str = "tmpl_home_bodyweight",
    schema_version: str = SCHEMA_VERSION,
    rule_set_version: str = "m04-provisional-1",
    catalog_version: str | None = None,
    declared_minutes: int | None = None,
    extra_items: list[tuple[str, int, IntensityPrescription]] | None = None,
    training_days: tuple[Weekday, ...] | None = None,
    sessions: tuple[DraftSession, ...] | None = None,
) -> TrainingPlanDraft:
    intensity = intensity or prescribe_intensity(goal, experience)
    items = [(exercise_id, working_sets, intensity)]
    if extra_items:
        items.extend(extra_items)
    if sessions is None:
        session = session_with_exercises(catalog, day, items, declared_minutes=declared_minutes)
        sessions = (session,)
        training_days = training_days or (day,)
    return TrainingPlanDraft(
        schema_version=schema_version,
        rule_set_version=rule_set_version,
        catalog_version=catalog_version or catalog.catalog_version,
        template_id=template_id,
        goal=goal,
        experience_level=experience,
        training_days=training_days or tuple(s.day for s in sessions),
        sessions=sessions,
        warnings=(),
        validation_status="PENDING",
        review_status="TECHNICAL_DRAFT_ONLY",
    )
