"""PostgreSQL persistence for synthetic_ai_memory (requires local DB)."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from app.modules.ai_memory.infrastructure.models import SyntheticAiMemoryRow


@pytest.mark.integration
def test_synthetic_memory_roundtrip(monkeypatch):
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql+psycopg://fitness:fitness_dev_only@127.0.0.1:15432/fitness_ai",
    )
    from app.core.config import Settings, clear_settings_cache

    clear_settings_cache()
    settings = Settings()  # type: ignore[call-arg]
    engine = create_engine(settings.database_url)
    mid = f"m_{uuid4().hex[:12]}"
    uid = "synth_persist_user"
    now = datetime.now(UTC)
    with Session(engine) as session:
        session.add(
            SyntheticAiMemoryRow(
                memory_id=mid,
                user_id=uid,
                memory_type="preferred_training_environment",
                key="environment",
                typed_value={"value": "home"},
                source_reference="integration",
                source_type="explicit_user",
                verification_status="explicit",
                status="active",
                created_at=now,
                updated_at=now,
                version=1,
            )
        )
        session.commit()

    # new session / engine = process-independent read
    engine2 = create_engine(settings.database_url)
    with Session(engine2) as session:
        row = session.get(SyntheticAiMemoryRow, mid)
        assert row is not None
        assert row.user_id == uid
        assert row.typed_value["value"] == "home"
        other = session.execute(
            text(
                "select count(*) from synthetic_ai_memory "
                "where user_id=:u and memory_id=:m and status='active'"
            ),
            {"u": "synth_other", "m": mid},
        ).scalar_one()
        assert other == 0
        row.status = "deleted"
        session.commit()

    with Session(engine2) as session:
        row = session.get(SyntheticAiMemoryRow, mid)
        assert row is not None
        assert row.status == "deleted"

    engine.dispose()
    engine2.dispose()
