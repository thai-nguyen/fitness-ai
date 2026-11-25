"""AI provider boundary unit tests (no network)."""

from app.core.ai_provider import resolve_ai_provider_config
from app.core.config import Settings


def test_resolve_ai_provider_config(monkeypatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://u:p@localhost:15432/db")
    monkeypatch.setenv("AI_PROVIDER", "ollama")
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    monkeypatch.setenv("OLLAMA_MODEL", "qwen3.5:9b")
    settings = Settings()  # type: ignore[call-arg]
    cfg = resolve_ai_provider_config(settings)
    assert cfg.provider == "ollama"
    assert cfg.model == "qwen3.5:9b"
    assert "192.168.8.54" not in cfg.base_url
