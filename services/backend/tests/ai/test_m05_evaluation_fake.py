from app.modules.ai_coach.domain.evaluation_m05 import build_m05_scenarios, run_m05_fake_evaluation


def test_m05_scenario_count_and_pass():
    assert len(build_m05_scenarios()) >= 50
    report = run_m05_fake_evaluation()
    assert report["functional_pass"] is True
    assert report["failed_scenario_ids"] == []
