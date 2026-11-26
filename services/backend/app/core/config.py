"""Typed environment configuration (pydantic-settings)."""

from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment / optional .env file."""

    model_config = SettingsConfigDict(
        # Prefer process env; optionally load repo-root or cwd .env (never commit secrets).
        env_file=("../../.env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = Field(default="fitness-ai-backend", alias="APP_NAME")
    app_env: Literal["development", "test", "staging", "production"] = Field(
        default="development", alias="APP_ENV"
    )
    app_version: str = Field(default="0.1.0", alias="APP_VERSION")
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8080, alias="PORT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    database_url: str = Field(alias="DATABASE_URL")

    ai_provider: str = Field(default="ollama", alias="AI_PROVIDER")
    ollama_base_url: str = Field(default="http://127.0.0.1:11434", alias="OLLAMA_BASE_URL")
    ollama_model: str = Field(default="qwen3.5:9b", alias="OLLAMA_MODEL")
    ai_connect_timeout_seconds: float = Field(default=5.0, alias="AI_CONNECT_TIMEOUT_SECONDS")
    ai_read_timeout_seconds: float = Field(default=120.0, alias="AI_READ_TIMEOUT_SECONDS")
    ai_total_timeout_seconds: float = Field(default=180.0, alias="AI_TOTAL_TIMEOUT_SECONDS")
    ai_max_output_tokens: int = Field(default=1024, alias="AI_MAX_OUTPUT_TOKENS")
    ai_max_context_tokens: int = Field(default=4096, alias="AI_MAX_CONTEXT_TOKENS")
    ai_max_repair_attempts: int = Field(default=1, alias="AI_MAX_REPAIR_ATTEMPTS")
    ai_max_concurrent_requests: int = Field(default=1, alias="AI_MAX_CONCURRENT_REQUESTS")
    ai_temperature: float = Field(default=0.2, alias="AI_TEMPERATURE")
    ai_poc_enabled: bool = Field(default=False, alias="AI_POC_ENABLED")

    @field_validator("database_url")
    @classmethod
    def database_url_must_be_present(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("DATABASE_URL is required")
        return value.strip()

    @field_validator("ollama_base_url")
    @classmethod
    def ollama_url_no_hardcoded_lan_requirement(cls, value: str) -> str:
        # Defaults intentionally use loopback placeholders; private LAN endpoints
        # belong only in ignored local .env files — never as committed defaults.
        return value.rstrip("/")


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


def clear_settings_cache() -> None:
    get_settings.cache_clear()
