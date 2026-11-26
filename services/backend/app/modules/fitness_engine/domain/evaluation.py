"""Synthetic evaluation scenarios for PH00-M04 technical feasibility.

All profiles are synthetic. Not clinical evaluation.
"""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter

from app.modules.exercise_catalog.domain.fixtures import load_fixture_catalog
from app.modules.exercise_catalog.domain.models import Equipment, ExerciseCatalog
from app.modules.fitness_engine.domain.assessment import AssessmentInput
from app.modules.fitness_engine.domain.enums import (
    ExperienceLevel,
    GenerationOutcome,
    Goal,
    Weekday,
)
from app.modules.fitness_engine.domain.generator import generate_training_plan


@dataclass(frozen=True)
class Scenario:
    scenario_id: str
    description: str
    assessment: AssessmentInput
    expected_outcomes: frozenset[GenerationOutcome]
    expected_rule_ids: tuple[str, ...]
    category: str  # positive | negative | boundary


def _a(**kwargs) -> AssessmentInput:
    base = dict(
        goal=Goal.GENERAL_FITNESS,
        experience_level=ExperienceLevel.BEGINNER,
        available_equipment=(Equipment.BODYWEIGHT,),
        available_training_days=(Weekday.MON, Weekday.WED, Weekday.FRI),
        preferred_training_days=(),
        max_session_duration_minutes=45,
        excluded_exercise_ids=(),
        known_exercise_restrictions=(),
        reported_pain_or_safety_concerns=(),
        adult_eligible=True,
        assessment_complete=True,
    )
    base.update(kwargs)
    return AssessmentInput(**base)


def build_scenarios() -> tuple[Scenario, ...]:
    gym_eq = (
        Equipment.BODYWEIGHT,
        Equipment.DUMBBELL,
        Equipment.BARBELL,
        Equipment.BENCH,
        Equipment.MACHINE,
        Equipment.CABLE,
    )
    home_eq = (Equipment.BODYWEIGHT, Equipment.DUMBBELL)
    return (
        Scenario(
            "S-POS-001",
            "Beginner general fitness",
            _a(),
            frozenset({GenerationOutcome.VALIDATED_TECHNICAL_DRAFT}),
            ("BR-ASSESS-001",),
            "positive",
        ),
        Scenario(
            "S-POS-002",
            "Beginner home workout",
            _a(available_equipment=(Equipment.BODYWEIGHT,)),
            frozenset({GenerationOutcome.VALIDATED_TECHNICAL_DRAFT}),
            ("BR-SEL-001",),
            "positive",
        ),
        Scenario(
            "S-POS-003",
            "Beginner gym workout",
            _a(
                goal=Goal.BEGINNER_STRENGTH,
                available_equipment=gym_eq,
                max_session_duration_minutes=60,
            ),
            frozenset({GenerationOutcome.VALIDATED_TECHNICAL_DRAFT}),
            ("BR-ASSESS-002",),
            "positive",
        ),
        Scenario(
            "S-POS-004",
            "Muscle gain goal",
            _a(
                goal=Goal.MUSCLE_GAIN,
                available_equipment=gym_eq,
                available_training_days=(Weekday.MON, Weekday.WED, Weekday.FRI),
                max_session_duration_minutes=60,
            ),
            frozenset({GenerationOutcome.VALIDATED_TECHNICAL_DRAFT}),
            ("BR-ASSESS-002",),
            "positive",
        ),
        Scenario(
            "S-POS-005",
            "Weight loss support",
            _a(goal=Goal.WEIGHT_LOSS_SUPPORT, available_equipment=home_eq),
            frozenset({GenerationOutcome.VALIDATED_TECHNICAL_DRAFT}),
            ("BR-ASSESS-002",),
            "positive",
        ),
        Scenario(
            "S-POS-006",
            "Limited equipment bodyweight",
            _a(available_equipment=(Equipment.BODYWEIGHT,)),
            frozenset({GenerationOutcome.VALIDATED_TECHNICAL_DRAFT}),
            ("BR-SEL-001",),
            "positive",
        ),
        Scenario(
            "S-POS-007",
            "Different availability 2 days",
            _a(available_training_days=(Weekday.TUE, Weekday.THU)),
            frozenset({GenerationOutcome.VALIDATED_TECHNICAL_DRAFT}),
            ("BR-SCHED-001",),
            "positive",
        ),
        Scenario(
            "S-POS-008",
            "Short session duration",
            _a(max_session_duration_minutes=25, available_equipment=(Equipment.BODYWEIGHT,)),
            frozenset(
                {
                    GenerationOutcome.VALIDATED_TECHNICAL_DRAFT,
                    GenerationOutcome.INFEASIBLE_CONSTRAINTS,
                }
            ),
            ("BR-DUR-002",),
            "positive",
        ),
        Scenario(
            "S-POS-009",
            "Intermediate general fitness",
            _a(experience_level=ExperienceLevel.INTERMEDIATE, available_equipment=home_eq),
            frozenset({GenerationOutcome.VALIDATED_TECHNICAL_DRAFT}),
            ("BR-SCOPE-001",),
            "positive",
        ),
        Scenario(
            "S-POS-010",
            "Preferred days honored subset",
            _a(preferred_training_days=(Weekday.MON, Weekday.FRI)),
            frozenset({GenerationOutcome.VALIDATED_TECHNICAL_DRAFT}),
            ("BR-SCHED-004",),
            "positive",
        ),
        Scenario(
            "S-NEG-001",
            "Missing goal",
            _a(goal=None),
            frozenset({GenerationOutcome.INVALID_INPUT}),
            ("BR-ASSESS-001",),
            "negative",
        ),
        Scenario(
            "S-NEG-002",
            "Invalid experience advanced",
            _a(experience_level=ExperienceLevel.ADVANCED),
            frozenset({GenerationOutcome.UNSUPPORTED_PROFILE}),
            ("BR-SCOPE-001",),
            "negative",
        ),
        Scenario(
            "S-NEG-003",
            "No available days",
            _a(available_training_days=()),
            frozenset({GenerationOutcome.INVALID_INPUT}),
            ("BR-SCHED-001",),
            "negative",
        ),
        Scenario(
            "S-NEG-004",
            "Invalid session duration",
            _a(max_session_duration_minutes=5),
            frozenset({GenerationOutcome.INVALID_INPUT}),
            ("BR-DUR-001",),
            "negative",
        ),
        Scenario(
            "S-NEG-005",
            "Non adult",
            _a(adult_eligible=False),
            frozenset({GenerationOutcome.UNSUPPORTED_PROFILE}),
            ("BR-SCOPE-002",),
            "negative",
        ),
        Scenario(
            "S-NEG-006",
            "Reported safety concern",
            _a(reported_pain_or_safety_concerns=("severe_chest_pain",)),
            frozenset({GenerationOutcome.REVIEW_REQUIRED}),
            ("BR-SAFE-002",),
            "negative",
        ),
        Scenario(
            "S-NEG-007",
            "Incomplete assessment",
            _a(assessment_complete=False),
            frozenset({GenerationOutcome.INVALID_INPUT}),
            ("BR-ASSESS-003",),
            "negative",
        ),
        Scenario(
            "S-NEG-008",
            "Duplicate days",
            _a(available_training_days=(Weekday.MON, Weekday.MON)),
            frozenset({GenerationOutcome.INVALID_INPUT}),
            ("BR-SCHED-002",),
            "negative",
        ),
        Scenario(
            "S-NEG-009",
            "Preferred not available",
            _a(preferred_training_days=(Weekday.SUN,)),
            frozenset({GenerationOutcome.INVALID_INPUT}),
            ("BR-SCHED-004",),
            "negative",
        ),
        Scenario(
            "S-NEG-010",
            "Missing adult eligibility",
            _a(adult_eligible=None),
            frozenset({GenerationOutcome.INVALID_INPUT}),
            ("BR-SAFE-001",),
            "negative",
        ),
        Scenario(
            "S-NEG-011",
            "Missing equipment",
            _a(available_equipment=()),
            frozenset({GenerationOutcome.INVALID_INPUT}),
            ("BR-ASSESS-001",),
            "negative",
        ),
        Scenario(
            "S-NEG-012",
            "Unsupported frequency >5",
            _a(
                available_training_days=(
                    Weekday.MON,
                    Weekday.TUE,
                    Weekday.WED,
                    Weekday.THU,
                    Weekday.FRI,
                    Weekday.SAT,
                )
            ),
            frozenset({GenerationOutcome.UNSUPPORTED_PROFILE, GenerationOutcome.INVALID_INPUT}),
            ("BR-SCHED-003",),
            "negative",
        ),
        Scenario(
            "S-NEG-013",
            "Excluded all squat options with knee restriction",
            _a(
                known_exercise_restrictions=(
                    "knee_pain",
                    "low_back_pain",
                    "shoulder_pain",
                    "wrist_pain",
                )
            ),
            frozenset(
                {GenerationOutcome.INSUFFICIENT_CATALOG, GenerationOutcome.INFEASIBLE_CONSTRAINTS}
            ),
            ("BR-SEL-004",),
            "negative",
        ),
        Scenario(
            "S-NEG-014",
            "Only kettlebell for strength-heavy template pressure",
            _a(
                goal=Goal.MUSCLE_GAIN,
                available_equipment=(Equipment.KETTLEBELL,),
                available_training_days=(Weekday.MON, Weekday.WED, Weekday.FRI),
            ),
            frozenset(
                {
                    GenerationOutcome.INSUFFICIENT_CATALOG,
                    GenerationOutcome.INFEASIBLE_CONSTRAINTS,
                    GenerationOutcome.VALIDATED_TECHNICAL_DRAFT,
                }
            ),
            ("BR-SEL-001",),
            "negative",
        ),
        Scenario(
            "S-BND-001",
            "Minimum supported availability 2 days",
            _a(available_training_days=(Weekday.SAT, Weekday.SUN)),
            frozenset({GenerationOutcome.VALIDATED_TECHNICAL_DRAFT}),
            ("BR-SCHED-001",),
            "boundary",
        ),
        Scenario(
            "S-BND-002",
            "Exact short duration window 20 min",
            _a(max_session_duration_minutes=20, available_equipment=(Equipment.BODYWEIGHT,)),
            frozenset(
                {
                    GenerationOutcome.VALIDATED_TECHNICAL_DRAFT,
                    GenerationOutcome.INFEASIBLE_CONSTRAINTS,
                }
            ),
            ("BR-DUR-002",),
            "boundary",
        ),
        Scenario(
            "S-BND-003",
            "Max fixture frequency 5 days",
            _a(
                available_training_days=(
                    Weekday.MON,
                    Weekday.TUE,
                    Weekday.WED,
                    Weekday.THU,
                    Weekday.FRI,
                ),
                available_equipment=gym_eq,
                goal=Goal.MUSCLE_GAIN,
                max_session_duration_minutes=60,
            ),
            frozenset(
                {
                    GenerationOutcome.VALIDATED_TECHNICAL_DRAFT,
                    GenerationOutcome.INFEASIBLE_CONSTRAINTS,
                }
            ),
            ("BR-SCHED-003",),
            "boundary",
        ),
        Scenario(
            "S-BND-004",
            "Band-only equipment",
            _a(available_equipment=(Equipment.RESISTANCE_BAND, Equipment.BODYWEIGHT)),
            frozenset(
                {
                    GenerationOutcome.VALIDATED_TECHNICAL_DRAFT,
                    GenerationOutcome.INSUFFICIENT_CATALOG,
                    GenerationOutcome.INFEASIBLE_CONSTRAINTS,
                }
            ),
            ("BR-SEL-001",),
            "boundary",
        ),
        Scenario(
            "S-BND-005",
            "Repeated identical generation determinism probe",
            _a(),
            frozenset({GenerationOutcome.VALIDATED_TECHNICAL_DRAFT}),
            ("BR-VAL-001",),
            "boundary",
        ),
        Scenario(
            "S-BND-006",
            "Contradictory exclusions of bodyweight squat id",
            _a(
                excluded_exercise_ids=(
                    "ex_bw_squat",
                    "ex_plank",
                    "ex_pushup",
                    "ex_bw_good_morning",
                    "ex_dead_bug",
                )
            ),
            frozenset(
                {
                    GenerationOutcome.INSUFFICIENT_CATALOG,
                    GenerationOutcome.INFEASIBLE_CONSTRAINTS,
                    GenerationOutcome.VALIDATED_TECHNICAL_DRAFT,
                }
            ),
            ("BR-SEL-004",),
            "boundary",
        ),
        Scenario(
            "S-BND-007",
            "Beginner strength home",
            _a(
                goal=Goal.BEGINNER_STRENGTH,
                available_equipment=(Equipment.BODYWEIGHT, Equipment.DUMBBELL),
            ),
            frozenset({GenerationOutcome.VALIDATED_TECHNICAL_DRAFT}),
            ("BR-ASSESS-002",),
            "boundary",
        ),
        Scenario(
            "S-NEG-015",
            "Missing duration",
            _a(max_session_duration_minutes=None),
            frozenset({GenerationOutcome.INVALID_INPUT}),
            ("BR-ASSESS-001",),
            "negative",
        ),
    )


@dataclass(frozen=True)
class ScenarioResult:
    scenario_id: str
    category: str
    expected_outcomes: tuple[str, ...]
    actual_outcome: str
    passed: bool
    rule_ids_seen: tuple[str, ...]
    latency_ms: float


def run_evaluation(catalog: ExerciseCatalog | None = None) -> list[ScenarioResult]:
    catalog = catalog or load_fixture_catalog()
    results: list[ScenarioResult] = []
    for sc in build_scenarios():
        t0 = perf_counter()
        if sc.scenario_id == "S-BND-005":
            r1 = generate_training_plan(sc.assessment, catalog)
            r2 = generate_training_plan(sc.assessment, catalog)
            same = (
                r1.outcome == r2.outcome
                and r1.draft is not None
                and r2.draft is not None
                and [e.exercise_id for s in r1.draft.sessions for e in s.exercises]
                == [e.exercise_id for s in r2.draft.sessions for e in s.exercises]
            )
            outcome = r1.outcome
            passed = same and outcome in sc.expected_outcomes
            issues = r1.issues
        else:
            result = generate_training_plan(sc.assessment, catalog)
            outcome = result.outcome
            passed = outcome in sc.expected_outcomes
            issues = result.issues
            if outcome == GenerationOutcome.VALIDATED_TECHNICAL_DRAFT and result.draft:
                # Hard constraint: no unknown IDs
                by_id = catalog.by_id()
                for session in result.draft.sessions:
                    for item in session.exercises:
                        if item.exercise_id not in by_id:
                            passed = False
        latency_ms = (perf_counter() - t0) * 1000
        results.append(
            ScenarioResult(
                scenario_id=sc.scenario_id,
                category=sc.category,
                expected_outcomes=tuple(sorted(o.value for o in sc.expected_outcomes)),
                actual_outcome=outcome.value,
                passed=passed,
                rule_ids_seen=tuple(sorted({i.rule_id for i in issues})),
                latency_ms=latency_ms,
            )
        )
    return results
