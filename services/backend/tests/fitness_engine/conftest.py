"""Shared fixtures for fitness engine unit tests (no DB/network)."""

from __future__ import annotations

import pytest

from app.modules.exercise_catalog.domain.fixtures import load_fixture_catalog
from app.modules.exercise_catalog.domain.models import Equipment
from app.modules.fitness_engine.domain.assessment import AssessmentInput
from app.modules.fitness_engine.domain.enums import ExperienceLevel, Goal, Weekday


@pytest.fixture
def catalog():
    return load_fixture_catalog()


@pytest.fixture
def beginner_home() -> AssessmentInput:
    return AssessmentInput(
        goal=Goal.GENERAL_FITNESS,
        experience_level=ExperienceLevel.BEGINNER,
        available_equipment=(Equipment.BODYWEIGHT,),
        available_training_days=(Weekday.MON, Weekday.WED, Weekday.FRI),
        preferred_training_days=(Weekday.MON, Weekday.WED),
        max_session_duration_minutes=45,
        adult_eligible=True,
        assessment_complete=True,
    )


@pytest.fixture
def beginner_gym() -> AssessmentInput:
    return AssessmentInput(
        goal=Goal.MUSCLE_GAIN,
        experience_level=ExperienceLevel.BEGINNER,
        available_equipment=(
            Equipment.BODYWEIGHT,
            Equipment.DUMBBELL,
            Equipment.BARBELL,
            Equipment.BENCH,
            Equipment.MACHINE,
            Equipment.CABLE,
        ),
        available_training_days=(Weekday.MON, Weekday.WED, Weekday.FRI),
        preferred_training_days=(Weekday.MON, Weekday.WED, Weekday.FRI),
        max_session_duration_minutes=60,
        adult_eligible=True,
        assessment_complete=True,
    )
