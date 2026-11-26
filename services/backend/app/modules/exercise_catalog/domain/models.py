"""Typed exercise catalog models (pure domain; no I/O)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class MuscleGroup(str, Enum):
    CHEST = "chest"
    BACK = "back"
    SHOULDERS = "shoulders"
    BICEPS = "biceps"
    TRICEPS = "triceps"
    QUADS = "quads"
    HAMSTRINGS = "hamstrings"
    GLUTES = "glutes"
    CALVES = "calves"
    CORE = "core"
    FULL_BODY = "full_body"


class MovementPattern(str, Enum):
    SQUAT = "squat"
    HINGE = "hinge"
    PUSH = "push"
    PULL = "pull"
    LUNGE = "lunge"
    CARRY = "carry"
    CORE = "core"
    CARDIO = "cardio"


class Equipment(str, Enum):
    BODYWEIGHT = "bodyweight"
    DUMBBELL = "dumbbell"
    BARBELL = "barbell"
    BENCH = "bench"
    CABLE = "cable"
    MACHINE = "machine"
    RESISTANCE_BAND = "resistance_band"
    KETTLEBELL = "kettlebell"
    PULL_UP_BAR = "pull_up_bar"


class Difficulty(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class ReviewStatus(str, Enum):
    TECHNICAL_FIXTURE = "technical_fixture"
    PENDING_REVIEW = "pending_review"
    REVIEWED = "reviewed"


class LicenseStatus(str, Enum):
    ORIGINAL_SYNTHETIC = "original_synthetic"
    UNVERIFIED = "unverified"
    OPEN_LICENSE_CANDIDATE = "open_license_candidate"


@dataclass(frozen=True)
class ExerciseDefinition:
    exercise_id: str
    name: str
    description: str
    primary_muscle_groups: tuple[MuscleGroup, ...]
    secondary_muscle_groups: tuple[MuscleGroup, ...]
    movement_pattern: MovementPattern
    equipment_requirements: tuple[Equipment, ...]
    difficulty: Difficulty
    instruction_steps: tuple[str, ...]
    contraindication_tags: tuple[str, ...]
    substitution_group: str
    estimated_duration_seconds: int
    media_reference: str | None
    content_source: str
    license_status: LicenseStatus
    review_status: ReviewStatus
    active_status: bool = True


@dataclass(frozen=True)
class ExerciseCatalog:
    catalog_version: str
    exercises: tuple[ExerciseDefinition, ...]

    def by_id(self) -> dict[str, ExerciseDefinition]:
        return {e.exercise_id: e for e in self.exercises}

    def active(self) -> tuple[ExerciseDefinition, ...]:
        return tuple(e for e in self.exercises if e.active_status)
