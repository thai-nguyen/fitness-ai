"""F-M04-004 duration estimation + independent validator verification."""

from __future__ import annotations

from app.modules.exercise_catalog.domain.models import Equipment
from app.modules.fitness_engine.domain.assessment import AssessmentInput
from app.modules.fitness_engine.domain.duration import (
    COOLDOWN_SECONDS,
    TRANSITION_SECONDS,
    WARMUP_SECONDS,
    estimate_minutes,
    estimate_session_seconds,
    fits_duration,
)
from app.modules.fitness_engine.domain.enums import ExperienceLevel, Goal, Weekday
from app.modules.fitness_engine.domain.intensity import prescribe_intensity
from app.modules.fitness_engine.domain.validator import validate_draft
from tests.fitness_engine.draft_helpers import make_draft


def test_duration_assumptions_documented(catalog):
    intensity = prescribe_intensity(Goal.GENERAL_FITNESS, ExperienceLevel.BEGINNER)
    ex = catalog.by_id()["ex_bw_squat"]
    seconds = estimate_session_seconds([(ex, 2, intensity)])
    expected = (
        WARMUP_SECONDS
        + COOLDOWN_SECONDS
        + ex.estimated_duration_seconds * 2
        + intensity.rest_seconds * 1
    )
    assert seconds == expected
    assert TRANSITION_SECONDS == 30


def test_duration_below_max(catalog):
    intensity = prescribe_intensity(Goal.GENERAL_FITNESS, ExperienceLevel.BEGINNER)
    ex = catalog.by_id()["ex_bw_squat"]
    minutes = estimate_minutes([(ex, 2, intensity)])
    assert fits_duration(minutes, minutes + 10)


def test_duration_exact_max(catalog):
    intensity = prescribe_intensity(Goal.GENERAL_FITNESS, ExperienceLevel.BEGINNER)
    ex = catalog.by_id()["ex_bw_squat"]
    minutes = estimate_minutes([(ex, 2, intensity)])
    assert fits_duration(minutes, minutes)
    a = AssessmentInput(
        goal=Goal.GENERAL_FITNESS,
        experience_level=ExperienceLevel.BEGINNER,
        available_equipment=(Equipment.BODYWEIGHT,),
        available_training_days=(Weekday.MON,),
        preferred_training_days=(),
        max_session_duration_minutes=minutes,
        adult_eligible=True,
    )
    draft = make_draft(catalog, day=Weekday.MON)
    issues = validate_draft(draft, catalog, a)
    assert not any(i.code == "SESSION_DURATION_VIOLATION" for i in issues)


def test_duration_above_max(catalog):
    a = AssessmentInput(
        goal=Goal.GENERAL_FITNESS,
        experience_level=ExperienceLevel.BEGINNER,
        available_equipment=(Equipment.BODYWEIGHT,),
        available_training_days=(Weekday.MON,),
        preferred_training_days=(),
        max_session_duration_minutes=1,
        adult_eligible=True,
    )
    draft = make_draft(catalog, day=Weekday.MON)
    issues = validate_draft(draft, catalog, a)
    assert any(i.code == "SESSION_DURATION_VIOLATION" for i in issues)


def test_declared_inconsistent_with_calculated(catalog, beginner_home):
    draft = make_draft(catalog, declared_minutes=999)
    issues = validate_draft(draft, catalog, beginner_home)
    assert any(i.code == "DECLARED_DURATION_MISMATCH" for i in issues)


def test_rounding_up_to_minutes(catalog):
    intensity = prescribe_intensity(Goal.GENERAL_FITNESS, ExperienceLevel.BEGINNER)
    ex = catalog.by_id()["ex_bw_squat"]
    seconds = estimate_session_seconds([(ex, 1, intensity)])
    minutes = estimate_minutes([(ex, 1, intensity)])
    assert minutes == (seconds + 59) // 60
