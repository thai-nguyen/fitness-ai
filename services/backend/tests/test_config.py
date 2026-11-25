"""Configuration unit tests."""

import pytest
from pydantic import ValidationError

from app.core.config import Settings, clear_settings_cache


def test_settings_require_database_url(monkeypatch: pytest.MonkeyPatch) -> None:
    clear_settings_cache()
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv("APP_ENV", "test")
    with pytest.raises(ValidationError):
        # Ignore local .env files so the test asserts env validation, not developer machine state.
        Settings(_env_file=None)  # type: ignore[call-arg]


def test_settings_load(monkeypatch: pytest.MonkeyPatch) -> None:
    clear_settings_cache()
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://u:p@localhost:15432/db")
    monkeypatch.setenv("APP_NAME", "fitness-ai-backend")
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    settings = Settings()  # type: ignore[call-arg]
    assert settings.app_name == "fitness-ai-backend"
    assert "15432" in settings.database_url
    assert "192.168.8.54" not in settings.ollama_base_url
