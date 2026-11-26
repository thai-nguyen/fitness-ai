from app.modules.ai_memory.domain.service import (
    InMemoryStore,
    MemoryApplicationService,
    MemoryError,
)


def test_memory_upsert_list_delete_isolation():
    svc = MemoryApplicationService(InMemoryStore())
    a = svc.propose_and_apply(
        trusted_user_id="synth_a",
        memory_type="preferred_training_environment",
        key="environment",
        value="home",
        source_reference="test",
    )
    svc.propose_and_apply(
        trusted_user_id="synth_b",
        memory_type="preferred_training_environment",
        key="environment",
        value="gym",
        source_reference="test",
    )
    assert [r.typed_value for r in svc.list_for_user("synth_a")] == ["home"]
    assert [r.typed_value for r in svc.list_for_user("synth_b")] == ["gym"]
    assert svc.delete_for_user("synth_a", a.memory_id) is True
    assert svc.list_for_user("synth_a") == []
    assert svc.list_for_user("synth_b")


def test_memory_rejects_untrusted_and_safety_keys():
    svc = MemoryApplicationService(InMemoryStore())
    try:
        svc.propose_and_apply(
            trusted_user_id="real_user",
            memory_type="preferred_training_environment",
            key="environment",
            value="home",
            source_reference="x",
        )
        raise AssertionError("expected failure")
    except MemoryError as exc:
        assert exc.code == "UNTRUSTED_USER"
    try:
        svc.propose_and_apply(
            trusted_user_id="synth_a",
            memory_type="preferred_training_environment",
            key="safety_restriction",
            value="home",
            source_reference="x",
        )
        raise AssertionError("expected failure")
    except MemoryError as exc:
        assert exc.code == "FORBIDDEN_KEY"


def test_authoritative_overrides_memory():
    svc = MemoryApplicationService(InMemoryStore())
    svc.propose_and_apply(
        trusted_user_id="synth_a",
        memory_type="preferred_session_duration_minutes",
        key="duration",
        value=45,
        source_reference="x",
    )
    merged = svc.resolve_conflicts(
        authoritative={"duration": 30},
        memories=svc.list_for_user("synth_a"),
    )
    assert merged["duration"] == 30
