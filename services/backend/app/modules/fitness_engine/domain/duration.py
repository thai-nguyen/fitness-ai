"""Session duration estimation (estimate ≠ actual workout duration)."""

from __future__ import annotations

from app.modules.exercise_catalog.domain.models import ExerciseDefinition
from app.modules.fitness_engine.domain.draft import IntensityPrescription

TRANSITION_SECONDS = 30
WARMUP_SECONDS = 180
COOLDOWN_SECONDS = 120


def estimate_session_seconds(
    exercises: list[tuple[ExerciseDefinition, int, IntensityPrescription]],
    include_warmup: bool = True,
) -> int:
    """Estimate total session seconds from exercises, sets, rest, transitions."""
    total = WARMUP_SECONDS + COOLDOWN_SECONDS if include_warmup else 0
    for i, (ex, working_sets, intensity) in enumerate(exercises):
        total += ex.estimated_duration_seconds * working_sets
        total += intensity.rest_seconds * max(working_sets - 1, 0)
        if i > 0:
            total += TRANSITION_SECONDS
    return total


def estimate_minutes(
    exercises: list[tuple[ExerciseDefinition, int, IntensityPrescription]],
) -> int:
    seconds = estimate_session_seconds(exercises)
    # Round up to whole minutes
    return (seconds + 59) // 60


def fits_duration(estimated_minutes: int, max_minutes: int) -> bool:
    return estimated_minutes <= max_minutes
