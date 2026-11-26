from app.modules.exercise_catalog.domain.models import Equipment, MovementPattern
from app.modules.fitness_engine.domain.enums import ExperienceLevel
from app.modules.fitness_engine.domain.selector import SelectionQuery, select_exercise


def test_selects_bodyweight_squat(catalog):
    q = SelectionQuery(
        movement_pattern=MovementPattern.SQUAT,
        available_equipment=frozenset({Equipment.BODYWEIGHT}),
        experience=ExperienceLevel.BEGINNER,
        excluded_ids=frozenset(),
        restriction_tags=frozenset(),
    )
    result = select_exercise(catalog, q)
    assert result.exercise is not None
    assert result.exercise.exercise_id == "ex_bw_squat"


def test_excludes_by_id(catalog):
    q = SelectionQuery(
        movement_pattern=MovementPattern.SQUAT,
        available_equipment=frozenset({Equipment.BODYWEIGHT}),
        experience=ExperienceLevel.BEGINNER,
        excluded_ids=frozenset({"ex_bw_squat"}),
        restriction_tags=frozenset(),
    )
    result = select_exercise(catalog, q)
    assert result.exercise is None or result.exercise.exercise_id != "ex_bw_squat"


def test_restriction_tag_blocks(catalog):
    q = SelectionQuery(
        movement_pattern=MovementPattern.SQUAT,
        available_equipment=frozenset({Equipment.BODYWEIGHT}),
        experience=ExperienceLevel.BEGINNER,
        excluded_ids=frozenset(),
        restriction_tags=frozenset({"knee_pain"}),
    )
    result = select_exercise(catalog, q)
    assert result.exercise is None


def test_beginner_cannot_get_advanced(catalog):
    q = SelectionQuery(
        movement_pattern=MovementPattern.SQUAT,
        available_equipment=frozenset({Equipment.BODYWEIGHT}),
        experience=ExperienceLevel.BEGINNER,
        excluded_ids=frozenset({"ex_bw_squat"}),
        restriction_tags=frozenset(),
    )
    result = select_exercise(catalog, q)
    if result.exercise:
        assert result.exercise.difficulty.value != "advanced"


def test_inactive_never_selected(catalog):
    q = SelectionQuery(
        movement_pattern=MovementPattern.PUSH,
        available_equipment=frozenset({Equipment.BODYWEIGHT}),
        experience=ExperienceLevel.BEGINNER,
        excluded_ids=frozenset(),
        restriction_tags=frozenset(),
    )
    result = select_exercise(catalog, q)
    assert result.exercise is not None
    assert result.exercise.exercise_id != "ex_inactive_demo"
