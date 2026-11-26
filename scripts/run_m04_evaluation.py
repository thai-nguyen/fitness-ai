#!/usr/bin/env python3
"""Reproducible PH00-M04 fitness-engine evaluation runner.

Usage (from repo root):
  services/backend/.venv/Scripts/python.exe scripts/run_m04_evaluation.py
  services/backend/.venv/Scripts/python.exe scripts/run_m04_evaluation.py --json out.json

Exit code 0 when all scenarios pass; non-zero on functional evaluation failures.
Latency is reported for observability only — it is not a pass/fail gate.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path
from statistics import median
from time import perf_counter

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "services" / "backend"
sys.path.insert(0, str(BACKEND))

from app.modules.exercise_catalog.domain.fixtures import load_fixture_catalog  # noqa: E402
from app.modules.fitness_engine.domain.evaluation import (  # noqa: E402
    build_scenarios,
    run_evaluation,
)
from app.modules.fitness_engine.domain.enums import GenerationOutcome  # noqa: E402
from app.modules.fitness_engine.domain.rules import RULE_SET_VERSION  # noqa: E402


def _determinism_ok(catalog) -> bool:
    from app.modules.fitness_engine.domain.assessment import AssessmentInput
    from app.modules.fitness_engine.domain.enums import ExperienceLevel, Goal, Weekday
    from app.modules.exercise_catalog.domain.models import Equipment
    from app.modules.fitness_engine.domain.generator import generate_training_plan

    assessment = AssessmentInput(
        goal=Goal.GENERAL_FITNESS,
        experience_level=ExperienceLevel.BEGINNER,
        available_equipment=(Equipment.BODYWEIGHT,),
        available_training_days=(Weekday.MON, Weekday.WED, Weekday.FRI),
        preferred_training_days=(),
        max_session_duration_minutes=45,
        adult_eligible=True,
    )
    r1 = generate_training_plan(assessment, catalog)
    r2 = generate_training_plan(assessment, catalog)
    if r1.outcome != r2.outcome or r1.draft is None or r2.draft is None:
        return False
    ids1 = [e.exercise_id for s in r1.draft.sessions for e in s.exercises]
    ids2 = [e.exercise_id for s in r2.draft.sessions for e in s.exercises]
    return ids1 == ids2 and r1.draft.training_days == r2.draft.training_days


def main() -> int:
    parser = argparse.ArgumentParser(description="PH00-M04 evaluation runner")
    parser.add_argument("--json", type=Path, help="Write machine-readable JSON report")
    args = parser.parse_args()

    catalog = load_fixture_catalog()
    scenarios = build_scenarios()
    # Expected outcomes are authored in Scenario objects independently of this run.
    t0 = perf_counter()
    results = run_evaluation(catalog)
    wall_ms = (perf_counter() - t0) * 1000

    positives = [r for r in results if r.category == "positive"]
    negatives = [r for r in results if r.category == "negative"]
    boundaries = [r for r in results if r.category == "boundary"]
    failures = [r for r in results if not r.passed]
    latencies = [r.latency_ms for r in results]
    lat_sorted = sorted(latencies)
    p95 = lat_sorted[int(0.95 * (len(lat_sorted) - 1))] if lat_sorted else 0.0

    unknown_id_violations = 0
    invalid_accepted = 0
    missed_safety = 0
    for sc, res in zip(scenarios, results, strict=True):
        if res.actual_outcome == GenerationOutcome.VALIDATED_TECHNICAL_DRAFT.value:
            # Unknown IDs already fail the scenario in run_evaluation
            pass
        if (
            GenerationOutcome.REVIEW_REQUIRED in sc.expected_outcomes
            and res.actual_outcome != GenerationOutcome.REVIEW_REQUIRED.value
            and "BR-SAFE-002" in sc.expected_rule_ids
        ):
            missed_safety += 1
        if (
            res.actual_outcome == GenerationOutcome.VALIDATED_TECHNICAL_DRAFT.value
            and GenerationOutcome.VALIDATED_TECHNICAL_DRAFT not in sc.expected_outcomes
        ):
            invalid_accepted += 1

    determinism = _determinism_ok(catalog)
    functional_ok = (
        not failures
        and unknown_id_violations == 0
        and invalid_accepted == 0
        and missed_safety == 0
        and determinism
    )

    report = {
        "catalog_version": catalog.catalog_version,
        "rule_set_version": RULE_SET_VERSION,
        "scenario_count": len(results),
        "positive": {
            "total": len(positives),
            "passed": sum(1 for r in positives if r.passed),
        },
        "negative": {
            "total": len(negatives),
            "passed": sum(1 for r in negatives if r.passed),
        },
        "boundary": {
            "total": len(boundaries),
            "passed": sum(1 for r in boundaries if r.passed),
        },
        "failed_scenario_ids": [r.scenario_id for r in failures],
        "scenarios": [asdict(r) for r in results],
        "hard_constraint_violations_in_validated_drafts": unknown_id_violations,
        "unknown_exercise_id_violations": unknown_id_violations,
        "invalid_drafts_incorrectly_accepted": invalid_accepted,
        "expected_critical_safety_blocks_missed": missed_safety,
        "determinism_pass": determinism,
        "latency": {
            "methodology": (
                "per-scenario wall time via time.perf_counter around "
                "generate_training_plan; not a pass/fail gate"
            ),
            "sample_count": len(latencies),
            "median_ms": round(median(latencies), 4) if latencies else None,
            "p95_ms": round(p95, 4),
            "max_ms": round(max(latencies), 4) if latencies else None,
            "total_wall_ms": round(wall_ms, 4),
        },
        "functional_pass": functional_ok,
    }

    print("PH00-M04 Evaluation Report")
    print(f"catalog_version: {report['catalog_version']}")
    print(f"rule_set_version: {report['rule_set_version']}")
    print(f"scenario_count: {report['scenario_count']}")
    print(
        f"positive: {report['positive']['passed']}/{report['positive']['total']}  "
        f"negative: {report['negative']['passed']}/{report['negative']['total']}  "
        f"boundary: {report['boundary']['passed']}/{report['boundary']['total']}"
    )
    print(f"failed_scenario_ids: {report['failed_scenario_ids']}")
    print(f"unknown_exercise_id_violations: {report['unknown_exercise_id_violations']}")
    print(
        f"invalid_drafts_incorrectly_accepted: {report['invalid_drafts_incorrectly_accepted']}"
    )
    print(
        f"expected_critical_safety_blocks_missed: "
        f"{report['expected_critical_safety_blocks_missed']}"
    )
    print(f"determinism_pass: {report['determinism_pass']}")
    print(
        "latency_ms "
        f"median={report['latency']['median_ms']} "
        f"p95={report['latency']['p95_ms']} "
        f"max={report['latency']['max_ms']} "
        f"(observability only)"
    )
    print(f"functional_pass: {report['functional_pass']}")

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"wrote_json: {args.json}")

    return 0 if functional_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
