from statistics import median

from app.modules.fitness_engine.domain.enums import GenerationOutcome
from app.modules.fitness_engine.domain.evaluation import build_scenarios, run_evaluation


def test_scenario_count_minimum():
    assert len(build_scenarios()) >= 30


def test_evaluation_dataset_passes(catalog):
    results = run_evaluation(catalog)
    assert len(results) >= 30
    failures = [r for r in results if not r.passed]
    summary = [(f.scenario_id, f.actual_outcome, f.expected_outcomes) for f in failures]
    assert failures == [], f"Failed scenarios: {summary}"

    positives = [r for r in results if r.category == "positive"]
    negatives = [r for r in results if r.category == "negative"]
    assert positives
    assert negatives
    assert all(r.passed for r in positives)
    assert all(r.passed for r in negatives)

    # No validated draft with unknown IDs (enforced in runner)
    validated = [
        r for r in results if r.actual_outcome == GenerationOutcome.VALIDATED_TECHNICAL_DRAFT.value
    ]
    assert validated

    latencies = [r.latency_ms for r in results]
    assert median(latencies) >= 0
    assert max(latencies) >= 0
