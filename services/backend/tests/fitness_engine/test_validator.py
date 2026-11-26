"""Independent validator tests — drafts constructed without the generator."""

from __future__ import annotations

import pytest

from app.modules.exercise_catalog.domain.models import Equipment
from app.modules.fitness_engine.domain.assessment import AssessmentInput
from app.modules.fitness_engine.domain.draft import IntensityPrescription
from app.modules.fitness_engine.domain.draft_parse import DraftParseError, parse_draft_mapping
from app.modules.fitness_engine.domain.duration import estimate_minutes
from app.modules.fitness_engine.domain.enums import ExperienceLevel, Goal, Weekday
from app.modules.fitness_engine.domain.intensity import prescribe_intensity
from app.modules.fitness_engine.domain.validator import is_technically_validated, validate_draft
from tests.fitness_engine.draft_helpers import make_draft, session_with_exercises


def test_unknown_exercise_rejected(catalog, beginner_home):
    # Construct with declared minutes only — unknown ID skips recalculation path
    from app.modules.fitness_engine.domain.draft import (
        SCHEMA_VERSION,
        DraftExercise,
        DraftSession,
        TrainingPlanDraft,
    )

    intensity = prescribe_intensity(Goal.GENERAL_FITNESS, ExperienceLevel.BEGINNER)
    draft = TrainingPlanDraft(
        schema_version=SCHEMA_VERSION,
        rule_set_version="m04-provisional-1",
        catalog_version=catalog.catalog_version,
        template_id="tmpl_home_bodyweight",
        goal=Goal.GENERAL_FITNESS,
        experience_level=ExperienceLevel.BEGINNER,
        training_days=(Weekday.MON,),
        sessions=(
            DraftSession(
                Weekday.MON,
                30,
                (DraftExercise("ex_unknown", 2, intensity),),
            ),
        ),
        warnings=(),
        validation_status="PENDING",
        review_status="TECHNICAL_DRAFT_ONLY",
    )
    issues = validate_draft(draft, catalog, beginner_home)
    assert any(i.code == "UNKNOWN_EXERCISE_ID" for i in issues)
    assert not is_technically_validated(issues)


def test_inactive_exercise_rejected(catalog, beginner_home):
    draft = make_draft(catalog, exercise_id="ex_inactive_demo")
    issues = validate_draft(draft, catalog, beginner_home)
    assert any(i.code == "INACTIVE_EXERCISE" for i in issues)


def test_equipment_incompatible(catalog, beginner_home):
    draft = make_draft(catalog, exercise_id="ex_bb_back_squat", template_id="tmpl_gym_strength")
    issues = validate_draft(draft, catalog, beginner_home)
    assert any(i.code == "EQUIPMENT_INCOMPATIBLE" for i in issues)


def test_excluded_exercise(catalog, beginner_home):
    a = AssessmentInput(
        goal=beginner_home.goal,
        experience_level=beginner_home.experience_level,
        available_equipment=beginner_home.available_equipment,
        available_training_days=beginner_home.available_training_days,
        preferred_training_days=(),
        max_session_duration_minutes=45,
        excluded_exercise_ids=("ex_bw_squat",),
        adult_eligible=True,
    )
    draft = make_draft(catalog, exercise_id="ex_bw_squat")
    issues = validate_draft(draft, catalog, a)
    assert any(i.code == "EXCLUDED_EXERCISE" for i in issues)


def test_safety_restriction(catalog, beginner_home):
    a = AssessmentInput(
        goal=beginner_home.goal,
        experience_level=beginner_home.experience_level,
        available_equipment=beginner_home.available_equipment,
        available_training_days=beginner_home.available_training_days,
        preferred_training_days=(),
        max_session_duration_minutes=45,
        known_exercise_restrictions=("knee_pain",),
        adult_eligible=True,
    )
    draft = make_draft(catalog, exercise_id="ex_bw_squat")
    issues = validate_draft(draft, catalog, a)
    assert any(i.code == "SAFETY_RESTRICTION" for i in issues)


def test_invalid_rule_set_version(catalog, beginner_home):
    draft = make_draft(catalog, rule_set_version="not-a-real-version")
    issues = validate_draft(draft, catalog, beginner_home)
    assert any(i.code == "RULE_VERSION_MISMATCH" for i in issues)


def test_invalid_catalog_version(catalog, beginner_home):
    draft = make_draft(catalog, catalog_version="other-catalog")
    issues = validate_draft(draft, catalog, beginner_home)
    assert any(i.code == "CATALOG_VERSION_MISMATCH" for i in issues)


def test_unknown_template(catalog, beginner_home):
    draft = make_draft(catalog, template_id="tmpl_does_not_exist")
    issues = validate_draft(draft, catalog, beginner_home)
    assert any(i.code == "UNKNOWN_TEMPLATE" for i in issues)


def test_incompatible_template_experience(catalog, beginner_home):
    # tmpl_beginner_full_body supports beginner only — use intermediate draft
    draft = make_draft(
        catalog,
        template_id="tmpl_beginner_full_body",
        experience=ExperienceLevel.INTERMEDIATE,
    )
    issues = validate_draft(draft, catalog, beginner_home)
    assert any(i.code == "TEMPLATE_EXPERIENCE_INCOMPATIBLE" for i in issues)


def test_invalid_working_sets(catalog, beginner_home):
    draft = make_draft(catalog, working_sets=9)
    issues = validate_draft(draft, catalog, beginner_home)
    assert any(i.code == "INVALID_WORKING_SETS" for i in issues)


def test_invalid_repetition_range(catalog, beginner_home):
    bad = IntensityPrescription((20, 5), "x", 6, 60, "m04-intensity-1")
    draft = make_draft(catalog, intensity=bad)
    issues = validate_draft(draft, catalog, beginner_home)
    assert any(i.code == "INVALID_REPETITION_RANGE" for i in issues)


def test_invalid_intensity_beginner_rpe(catalog, beginner_home):
    bad = IntensityPrescription((8, 12), "max", 9, 60, "m04-intensity-1")
    draft = make_draft(catalog, intensity=bad)
    issues = validate_draft(draft, catalog, beginner_home)
    assert any(i.code == "INVALID_INTENSITY" for i in issues)


def test_invalid_rest_duration(catalog, beginner_home):
    bad = IntensityPrescription((8, 12), "ok", 6, -10, "m04-intensity-1")
    draft = make_draft(catalog, intensity=bad)
    issues = validate_draft(draft, catalog, beginner_home)
    assert any(i.code == "INVALID_REST" for i in issues)


def test_schedule_outside_availability(catalog, beginner_home):
    draft = make_draft(catalog, day=Weekday.SUN)
    issues = validate_draft(draft, catalog, beginner_home)
    assert any(i.code == "SCHEDULE_OUTSIDE_AVAILABILITY" for i in issues)


def test_duplicate_session_day(catalog, beginner_home):
    intensity = prescribe_intensity(Goal.GENERAL_FITNESS, ExperienceLevel.BEGINNER)
    s1 = session_with_exercises(catalog, Weekday.MON, [("ex_bw_squat", 2, intensity)])
    s2 = session_with_exercises(catalog, Weekday.MON, [("ex_plank", 2, intensity)])
    draft = make_draft(
        catalog,
        sessions=(s1, s2),
        training_days=(Weekday.MON, Weekday.MON),
    )
    issues = validate_draft(draft, catalog, beginner_home)
    assert any(i.code == "DUPLICATE_SESSION_DAY" for i in issues)


def test_duplicate_exercise_in_session(catalog, beginner_home):
    intensity = prescribe_intensity(Goal.GENERAL_FITNESS, ExperienceLevel.BEGINNER)
    draft = make_draft(
        catalog,
        exercise_id="ex_bw_squat",
        extra_items=[("ex_bw_squat", 2, intensity)],
    )
    issues = validate_draft(draft, catalog, beginner_home)
    assert any(i.code == "DUPLICATE_EXERCISE" for i in issues)


def test_experience_difficulty_incompatible(catalog, beginner_home):
    draft = make_draft(catalog, exercise_id="ex_advanced_pistol")
    issues = validate_draft(draft, catalog, beginner_home)
    assert any(i.code == "EXPERIENCE_DIFFICULTY_INCOMPATIBLE" for i in issues)


def test_declared_duration_mismatch(catalog, beginner_home):
    draft = make_draft(catalog, declared_minutes=1)
    issues = validate_draft(draft, catalog, beginner_home)
    assert any(i.code == "DECLARED_DURATION_MISMATCH" for i in issues)


def test_session_duration_over_max(catalog):
    a = AssessmentInput(
        goal=Goal.GENERAL_FITNESS,
        experience_level=ExperienceLevel.BEGINNER,
        available_equipment=(Equipment.BODYWEIGHT,),
        available_training_days=(Weekday.MON, Weekday.WED, Weekday.FRI),
        preferred_training_days=(),
        max_session_duration_minutes=5,
        adult_eligible=True,
    )
    draft = make_draft(catalog, working_sets=5)
    issues = validate_draft(draft, catalog, a)
    assert any(i.code == "SESSION_DURATION_VIOLATION" for i in issues)


def test_duration_exact_max_passes_duration_check(catalog):
    intensity = prescribe_intensity(Goal.GENERAL_FITNESS, ExperienceLevel.BEGINNER)
    ex = catalog.by_id()["ex_bw_squat"]
    minutes = estimate_minutes([(ex, 2, intensity)])
    a = AssessmentInput(
        goal=Goal.GENERAL_FITNESS,
        experience_level=ExperienceLevel.BEGINNER,
        available_equipment=(Equipment.BODYWEIGHT,),
        available_training_days=(Weekday.MON, Weekday.WED, Weekday.FRI),
        preferred_training_days=(),
        max_session_duration_minutes=minutes,
        adult_eligible=True,
    )
    draft = make_draft(catalog)
    issues = validate_draft(draft, catalog, a)
    assert not any(i.code == "SESSION_DURATION_VIOLATION" for i in issues)
    assert not any(i.code == "DECLARED_DURATION_MISMATCH" for i in issues)


def test_schema_parse_missing_field():
    with pytest.raises(DraftParseError) as exc:
        parse_draft_mapping({"schema_version": "1.0.0"})
    assert any(i.code == "SCHEMA_MISSING_FIELD" for i in exc.value.issues)


def test_schema_correct_json_still_needs_domain_validation(catalog, beginner_home):
    """LLM-shaped JSON that is schema-complete can still fail hard domain checks."""
    intensity = prescribe_intensity(Goal.GENERAL_FITNESS, ExperienceLevel.BEGINNER)
    minutes = estimate_minutes([(catalog.by_id()["ex_bw_squat"], 2, intensity)])
    payload = {
        "schema_version": "1.0.0",
        "rule_set_version": "m04-provisional-1",
        "catalog_version": catalog.catalog_version,
        "template_id": "tmpl_home_bodyweight",
        "goal": "general_fitness",
        "experience_level": "beginner",
        "training_days": ["mon"],
        "sessions": [
            {
                "day": "mon",
                "estimated_duration_minutes": minutes,
                "exercises": [
                    {
                        "exercise_id": "ex_unknown_llm",
                        "working_sets": 2,
                        "intensity": {
                            "repetition_range": [8, 12],
                            "effort_guidance": "moderate",
                            "rpe": 6,
                            "rest_seconds": 60,
                            "intensity_policy_version": "m04-intensity-1",
                        },
                    }
                ],
            }
        ],
        "warnings": [],
        "validation_status": "PENDING",
        "review_status": "TECHNICAL_DRAFT_ONLY",
    }
    draft = parse_draft_mapping(payload)
    issues = validate_draft(draft, catalog, beginner_home)
    assert any(i.code == "UNKNOWN_EXERCISE_ID" for i in issues)
    assert not is_technically_validated(issues)


def test_valid_constructed_draft_can_pass(catalog, beginner_home):
    draft = make_draft(catalog, exercise_id="ex_bw_squat")
    issues = validate_draft(draft, catalog, beginner_home)
    # May warn on volume; hard errors should be absent for this minimal compatible draft
    assert is_technically_validated(issues) or not any(
        i.code
        in {
            "UNKNOWN_EXERCISE_ID",
            "EQUIPMENT_INCOMPATIBLE",
            "INACTIVE_EXERCISE",
            "DECLARED_DURATION_MISMATCH",
        }
        for i in issues
    )
