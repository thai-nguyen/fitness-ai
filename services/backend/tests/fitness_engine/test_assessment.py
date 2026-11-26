from app.modules.exercise_catalog.domain.models import Equipment
from app.modules.fitness_engine.domain.assessment import AssessmentInput, validate_assessment
from app.modules.fitness_engine.domain.enums import ExperienceLevel, Goal, Weekday


def test_valid_assessment(beginner_home):
    assert validate_assessment(beginner_home) == []


def test_missing_goal():
    a = AssessmentInput(
        goal=None,
        experience_level=ExperienceLevel.BEGINNER,
        available_equipment=(Equipment.BODYWEIGHT,),
        available_training_days=(Weekday.MON,),
        preferred_training_days=(),
        max_session_duration_minutes=30,
        adult_eligible=True,
    )
    codes = {i.code for i in validate_assessment(a)}
    assert "MISSING_GOAL" in codes


def test_unsupported_experience():
    a = AssessmentInput(
        goal=Goal.GENERAL_FITNESS,
        experience_level=ExperienceLevel.ADVANCED,
        available_equipment=(Equipment.BODYWEIGHT,),
        available_training_days=(Weekday.MON, Weekday.WED),
        preferred_training_days=(),
        max_session_duration_minutes=30,
        adult_eligible=True,
    )
    codes = {i.code for i in validate_assessment(a)}
    assert "UNSUPPORTED_EXPERIENCE" in codes


def test_no_available_days():
    a = AssessmentInput(
        goal=Goal.GENERAL_FITNESS,
        experience_level=ExperienceLevel.BEGINNER,
        available_equipment=(Equipment.BODYWEIGHT,),
        available_training_days=(),
        preferred_training_days=(),
        max_session_duration_minutes=30,
        adult_eligible=True,
    )
    assert any(i.code == "NO_AVAILABLE_DAYS" for i in validate_assessment(a))


def test_invalid_session_duration():
    a = AssessmentInput(
        goal=Goal.GENERAL_FITNESS,
        experience_level=ExperienceLevel.BEGINNER,
        available_equipment=(Equipment.BODYWEIGHT,),
        available_training_days=(Weekday.MON,),
        preferred_training_days=(),
        max_session_duration_minutes=10,
        adult_eligible=True,
    )
    assert any(i.code == "INVALID_SESSION_DURATION" for i in validate_assessment(a))
