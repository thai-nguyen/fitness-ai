from app.modules.fitness_engine.domain.traceability import compute_traceability_metrics


def test_traceability_metrics_resolve():
    m = compute_traceability_metrics()
    assert m.total_documented_rules >= 20
    assert m.expert_approved_rules == 0
    assert m.rules_with_verified_executable_tests == m.rules_with_test_ref
    assert m.unresolved_test_refs == ()
    assert m.rules_missing_negative_hard_tests == ()
