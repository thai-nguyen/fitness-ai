"""F-M04-002 safety fail-closed evidence (technical screening only)."""

from __future__ import annotations

from app.modules.exercise_catalog.domain.models import Equipment
from app.modules.fitness_engine.domain.assessment import AssessmentInput
from app.modules.fitness_engine.domain.enums import (
    ExperienceLevel,
    GenerationOutcome,
    Goal,
    SafetyOutcome,
    Weekday,
)
from app.modules.fitness_engine.domain.generator import generate_training_plan
from app.modules.fitness_engine.domain.safety import screen_safety
from app.modules.fitness_engine.domain.substitution import find_substitute
from app.modules.fitness_engine.domain.validator import validate_draft
from tests.fitness_engine.draft_helpers import make_draft


def _base(**kwargs) -> AssessmentInput:
    data = dict(
        goal=Goal.GENERAL_FITNESS,
        experience_level=ExperienceLevel.BEGINNER,
        available_equipment=(Equipment.BODYWEIGHT, Equipment.DUMBBELL),
        available_training_days=(Weekday.MON, Weekday.WED, Weekday.FRI),
        preferred_training_days=(Weekday.MON, Weekday.WED),
        max_session_duration_minutes=45,
        excluded_exercise_ids=(),
        known_exercise_restrictions=(),
        reported_pain_or_safety_concerns=(),
        adult_eligible=True,
        assessment_complete=True,
    )
    data.update(kwargs)
    return AssessmentInput(**data)


def test_missing_adult_not_treated_as_safe():
    result = screen_safety(_base(adult_eligible=None))
    assert result.outcome == SafetyOutcome.INSUFFICIENT_INFORMATION


def test_missing_safety_config_fail_closed():
    assert screen_safety(_base(), rule_set_version=None).outcome == SafetyOutcome.REJECTED


def test_reported_symptoms_not_bypassed_by_preferences(catalog):
    a = _base(
        reported_pain_or_safety_concerns=("chest_pain",),
        preferred_training_days=(Weekday.MON, Weekday.WED, Weekday.FRI),
        available_equipment=(
            Equipment.BODYWEIGHT,
            Equipment.DUMBBELL,
            Equipment.BARBELL,
            Equipment.BENCH,
            Equipment.MACHINE,
            Equipment.CABLE,
        ),
        max_session_duration_minutes=90,
    )
    result = generate_training_plan(a, catalog)
    assert result.outcome == GenerationOutcome.REVIEW_REQUIRED
    assert result.draft is None


def test_non_adult_not_bypassed_by_template_preference(catalog):
    a = _base(adult_eligible=False, goal=Goal.MUSCLE_GAIN)
    result = generate_training_plan(a, catalog)
    assert result.outcome == GenerationOutcome.UNSUPPORTED_PROFILE
    assert result.draft is None


def test_restrictions_block_even_with_gym_equipment(catalog):
    a = _base(
        known_exercise_restrictions=(
            "knee_pain",
            "low_back_pain",
            "shoulder_pain",
            "wrist_pain",
        ),
        available_equipment=(
            Equipment.BODYWEIGHT,
            Equipment.DUMBBELL,
            Equipment.BARBELL,
            Equipment.BENCH,
            Equipment.MACHINE,
            Equipment.CABLE,
        ),
    )
    result = generate_training_plan(a, catalog)
    assert result.outcome in {
        GenerationOutcome.INSUFFICIENT_CATALOG,
        GenerationOutcome.INFEASIBLE_CONSTRAINTS,
    }
    assert result.draft is None


def test_substitution_cannot_bypass_restriction_tags(catalog):
    result = find_substitute(
        catalog,
        "ex_bw_squat",
        (Equipment.BODYWEIGHT, Equipment.DUMBBELL),
        ExperienceLevel.BEGINNER,
        restriction_tags=("knee_pain",),
    )
    assert result.valid is False


def test_validator_enforces_restriction_when_draft_bypasses_generator(catalog):
    a = _base(known_exercise_restrictions=("knee_pain",))
    draft = make_draft(catalog, exercise_id="ex_bw_squat")
    issues = validate_draft(draft, catalog, a)
    assert any(i.code == "SAFETY_RESTRICTION" for i in issues)


def test_conflicting_preferred_not_available_invalid_input(catalog):
    a = _base(preferred_training_days=(Weekday.SUN,))
    result = generate_training_plan(a, catalog)
    assert result.outcome == GenerationOutcome.INVALID_INPUT


def test_incomplete_assessment_insufficient():
    assert (
        screen_safety(_base(assessment_complete=False)).outcome
        == SafetyOutcome.INSUFFICIENT_INFORMATION
    )
