from app.modules.exercise_catalog.domain.models import Equipment
from app.modules.fitness_engine.domain.assessment import AssessmentInput
from app.modules.fitness_engine.domain.enums import ExperienceLevel, Goal, SafetyOutcome, Weekday
from app.modules.fitness_engine.domain.safety import screen_safety


def _base(**kwargs) -> AssessmentInput:
    data = dict(
        goal=Goal.GENERAL_FITNESS,
        experience_level=ExperienceLevel.BEGINNER,
        available_equipment=(Equipment.BODYWEIGHT,),
        available_training_days=(Weekday.MON, Weekday.WED),
        preferred_training_days=(),
        max_session_duration_minutes=40,
        adult_eligible=True,
        assessment_complete=True,
    )
    data.update(kwargs)
    return AssessmentInput(**data)


def test_safety_pass():
    assert screen_safety(_base()).outcome == SafetyOutcome.PASSED_TECHNICAL_CHECKS


def test_reported_concern_blocks():
    result = screen_safety(_base(reported_pain_or_safety_concerns=("chest_pain",)))
    assert result.outcome == SafetyOutcome.REVIEW_REQUIRED
    assert result.guidance_category == "professional_review_or_urgent_care_guidance"


def test_non_adult_rejected():
    result = screen_safety(_base(adult_eligible=False))
    assert result.outcome == SafetyOutcome.REJECTED


def test_missing_adult_insufficient():
    result = screen_safety(_base(adult_eligible=None))
    assert result.outcome == SafetyOutcome.INSUFFICIENT_INFORMATION


def test_missing_rule_config_fail_closed():
    result = screen_safety(_base(), rule_set_version=None)
    assert result.outcome == SafetyOutcome.REJECTED
    assert any(i.code == "MISSING_SAFETY_CONFIGURATION" for i in result.issues)
