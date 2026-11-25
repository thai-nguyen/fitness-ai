"""Pytest fixtures for backend foundation tests."""

from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

# Default test DB uses project-specific host port; override via env if needed.
DEFAULT_TEST_DB = "postgresql+psycopg://fitness:fitness_dev_only@127.0.0.1:15432/fitness_ai"


@pytest.fixture()
def test_env(monkeypatch: pytest.MonkeyPatch) -> dict[str, str]:
    env = {
        "APP_NAME": "fitness-ai-backend",
        "APP_ENV": "test",
        "APP_VERSION": "0.1.0",
        "LOG_LEVEL": "WARNING",
        "DATABASE_URL": os.environ.get("DATABASE_URL", DEFAULT_TEST_DB),
        "AI_PROVIDER": "ollama",
        "OLLAMA_BASE_URL": "http://127.0.0.1:11434",
        "OLLAMA_MODEL": "qwen3.5:9b",
    }
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    return env


@pytest.fixture()
def client(test_env: dict[str, str], monkeypatch: pytest.MonkeyPatch) -> TestClient:
    from app.core.config import clear_settings_cache
    from app.main import create_app

    clear_settings_cache()
    app = create_app()
    with TestClient(app) as test_client:
        yield test_client
    clear_settings_cache()


@pytest.fixture()
def unavailable_db_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    from app.core.config import clear_settings_cache
    from app.main import create_app

    monkeypatch.setenv("APP_NAME", "fitness-ai-backend")
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("APP_VERSION", "0.1.0")
    monkeypatch.setenv("LOG_LEVEL", "WARNING")
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql+psycopg://fitness:fitness_dev_only@127.0.0.1:1/fitness_ai",
    )
    monkeypatch.setenv("AI_PROVIDER", "ollama")
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    monkeypatch.setenv("OLLAMA_MODEL", "qwen3.5:9b")
    clear_settings_cache()
    app = create_app()
    with TestClient(app) as test_client:
        yield test_client
    clear_settings_cache()


def database_reachable(url: str) -> bool:
    try:
        engine = create_engine(url, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        engine.dispose()
        return True
    except Exception:
        return False
