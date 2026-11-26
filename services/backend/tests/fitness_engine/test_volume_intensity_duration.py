from app.modules.fitness_engine.domain.draft import (
    SCHEMA_VERSION,
    DraftExercise,
    DraftSession,
    IntensityPrescription,
    TrainingPlanDraft,
)
from app.modules.fitness_engine.domain.duration import estimate_minutes, fits_duration
from app.modules.fitness_engine.domain.enums import ExperienceLevel, Goal, Weekday
from app.modules.fitness_engine.domain.intensity import prescribe_intensity, validate_intensity
from app.modules.fitness_engine.domain.volume import validate_working_sets, volume_issues


def test_working_sets_bounds():
    assert validate_working_sets(0) is not None
    assert validate_working_sets(6) is not None
    assert validate_working_sets(3) is None


def test_intensity_beginner_rpe_cap():
    bad = IntensityPrescription(
        repetition_range=(8, 12),
        effort_guidance="max",
        rpe=9,
        rest_seconds=60,
        intensity_policy_version="m04-intensity-1",
    )
    issues = validate_intensity(bad, ExperienceLevel.BEGINNER)
    assert any(i.code == "INVALID_INTENSITY" for i in issues)


def test_invalid_rep_range():
    bad = IntensityPrescription(
        repetition_range=(12, 8),
        effort_guidance="x",
        rpe=6,
        rest_seconds=60,
        intensity_policy_version="m04-intensity-1",
    )
    assert any(
        i.code == "INVALID_REPETITION_RANGE"
        for i in validate_intensity(bad, ExperienceLevel.BEGINNER)
    )


def test_duration_estimate(catalog):
    intensity = prescribe_intensity(Goal.GENERAL_FITNESS, ExperienceLevel.BEGINNER)
    ex = catalog.by_id()["ex_bw_squat"]
    minutes = estimate_minutes([(ex, 2, intensity)])
    assert minutes > 0
    assert fits_duration(minutes, 90)
    assert not fits_duration(minutes, 1)


def test_volume_excessive_error(catalog):
    intensity = prescribe_intensity(Goal.MUSCLE_GAIN, ExperienceLevel.INTERMEDIATE)
    # Craft many sets of same primary muscle across sessions
    item = DraftExercise("ex_bw_squat", working_sets=5, intensity=intensity)
    sessions = tuple(
        DraftSession(day=d, estimated_duration_minutes=40, exercises=(item,))
        for d in (
            Weekday.MON,
            Weekday.TUE,
            Weekday.WED,
            Weekday.THU,
            Weekday.FRI,
            Weekday.SAT,
            Weekday.SUN,
        )
    )
    draft = TrainingPlanDraft(
        schema_version=SCHEMA_VERSION,
        rule_set_version="m04-provisional-1",
        catalog_version=catalog.catalog_version,
        template_id="tmpl_general_fitness",
        goal=Goal.GENERAL_FITNESS,
        experience_level=ExperienceLevel.INTERMEDIATE,
        training_days=tuple(s.day for s in sessions),
        sessions=sessions,
        warnings=(),
        validation_status="PENDING",
        review_status="TECHNICAL_DRAFT_ONLY",
    )
    issues = volume_issues(draft, catalog)
    assert any(i.code == "EXCESSIVE_VOLUME" for i in issues)
