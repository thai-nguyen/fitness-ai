from app.modules.exercise_catalog.domain.models import Equipment
from app.modules.fitness_engine.domain.enums import ExperienceLevel
from app.modules.fitness_engine.domain.substitution import find_substitute


def test_find_substitute_same_group(catalog):
    result = find_substitute(
        catalog,
        "ex_bw_squat",
        (Equipment.BODYWEIGHT, Equipment.DUMBBELL),
        ExperienceLevel.BEGINNER,
    )
    assert result.valid
    assert result.replacement_exercise_id == "ex_goblet_squat"


def test_no_substitute(catalog):
    result = find_substitute(
        catalog,
        "ex_bw_squat",
        (Equipment.BODYWEIGHT,),
        ExperienceLevel.BEGINNER,
        excluded_ids=("ex_goblet_squat",),
        restriction_tags=("knee_pain",),
    )
    # knee_pain blocks all squat_basic bodyweight/db options remaining
    assert result.valid is False
    assert result.reason in {"NO_SUBSTITUTE", "UNKNOWN_ORIGINAL"}


def test_unknown_original(catalog):
    result = find_substitute(
        catalog,
        "ex_does_not_exist",
        (Equipment.BODYWEIGHT,),
        ExperienceLevel.BEGINNER,
    )
    assert result.valid is False
    assert result.reason == "UNKNOWN_ORIGINAL"
