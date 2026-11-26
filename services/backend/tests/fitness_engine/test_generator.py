from app.modules.exercise_catalog.domain.models import Equipment
from app.modules.fitness_engine.domain.assessment import AssessmentInput
from app.modules.fitness_engine.domain.enums import (
    ExperienceLevel,
    GenerationOutcome,
    Goal,
    Weekday,
)
from app.modules.fitness_engine.domain.generator import generate_training_plan


def test_positive_home_generation(catalog, beginner_home):
    result = generate_training_plan(beginner_home, catalog)
    assert result.outcome == GenerationOutcome.VALIDATED_TECHNICAL_DRAFT
    assert result.draft is not None
    assert result.draft.validation_status == "VALIDATED_TECHNICAL_DRAFT"
    ids = {e.exercise_id for s in result.draft.sessions for e in s.exercises}
    assert "ex_unknown" not in ids
    assert all(catalog.by_id()[i].active_status for i in ids)


def test_positive_gym_generation(catalog, beginner_gym):
    result = generate_training_plan(beginner_gym, catalog)
    assert result.outcome == GenerationOutcome.VALIDATED_TECHNICAL_DRAFT
    assert result.draft is not None


def test_safety_concern_review_required(catalog, beginner_home):
    a = AssessmentInput(
        goal=beginner_home.goal,
        experience_level=beginner_home.experience_level,
        available_equipment=beginner_home.available_equipment,
        available_training_days=beginner_home.available_training_days,
        preferred_training_days=beginner_home.preferred_training_days,
        max_session_duration_minutes=beginner_home.max_session_duration_minutes,
        adult_eligible=True,
        reported_pain_or_safety_concerns=("dizziness",),
    )
    result = generate_training_plan(a, catalog)
    assert result.outcome == GenerationOutcome.REVIEW_REQUIRED
    assert result.draft is None


def test_unsupported_advanced(catalog):
    a = AssessmentInput(
        goal=Goal.GENERAL_FITNESS,
        experience_level=ExperienceLevel.ADVANCED,
        available_equipment=(Equipment.BODYWEIGHT,),
        available_training_days=(Weekday.MON, Weekday.WED),
        preferred_training_days=(),
        max_session_duration_minutes=40,
        adult_eligible=True,
    )
    result = generate_training_plan(a, catalog)
    assert result.outcome == GenerationOutcome.UNSUPPORTED_PROFILE


def test_insufficient_catalog_equipment(catalog):
    a = AssessmentInput(
        goal=Goal.MUSCLE_GAIN,
        experience_level=ExperienceLevel.BEGINNER,
        available_equipment=(Equipment.KETTLEBELL,),  # limited for gym strength template slots
        available_training_days=(Weekday.MON, Weekday.WED, Weekday.FRI),
        preferred_training_days=(),
        max_session_duration_minutes=60,
        adult_eligible=True,
    )
    result = generate_training_plan(a, catalog)
    assert result.outcome in {
        GenerationOutcome.INSUFFICIENT_CATALOG,
        GenerationOutcome.INFEASIBLE_CONSTRAINTS,
        GenerationOutcome.VALIDATED_TECHNICAL_DRAFT,
    }
    # If validated, must not contain unknown IDs
    if result.draft:
        for s in result.draft.sessions:
            for e in s.exercises:
                assert e.exercise_id in catalog.by_id()


def test_determinism(catalog, beginner_home):
    r1 = generate_training_plan(beginner_home, catalog)
    r2 = generate_training_plan(beginner_home, catalog)
    assert r1.outcome == r2.outcome == GenerationOutcome.VALIDATED_TECHNICAL_DRAFT
    assert r1.draft is not None and r2.draft is not None
    assert r1.draft.template_id == r2.draft.template_id
    assert r1.draft.training_days == r2.draft.training_days
    for s1, s2 in zip(r1.draft.sessions, r2.draft.sessions, strict=True):
        assert s1.day == s2.day
        assert [e.exercise_id for e in s1.exercises] == [e.exercise_id for e in s2.exercises]
        assert [e.working_sets for e in s1.exercises] == [e.working_sets for e in s2.exercises]
