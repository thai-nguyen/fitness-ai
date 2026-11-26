"""Training plan draft contract (technical drafts only; never activated in M04)."""

from __future__ import annotations

from dataclasses import dataclass

from app.modules.fitness_engine.domain.enums import ExperienceLevel, Goal, Weekday

SCHEMA_VERSION = "1.0.0"


@dataclass(frozen=True)
class IntensityPrescription:
    repetition_range: tuple[int, int]
    effort_guidance: str
    rpe: int | None
    rest_seconds: int
    intensity_policy_version: str


@dataclass(frozen=True)
class DraftExercise:
    exercise_id: str
    working_sets: int
    intensity: IntensityPrescription


@dataclass(frozen=True)
class DraftSession:
    day: Weekday
    estimated_duration_minutes: int
    exercises: tuple[DraftExercise, ...]


@dataclass(frozen=True)
class TrainingPlanDraft:
    schema_version: str
    rule_set_version: str
    catalog_version: str
    template_id: str
    goal: Goal
    experience_level: ExperienceLevel
    training_days: tuple[Weekday, ...]
    sessions: tuple[DraftSession, ...]
    warnings: tuple[str, ...]
    validation_status: str
    review_status: str
