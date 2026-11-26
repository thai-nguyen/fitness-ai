"""Structured AI provider error categories (no raw provider leakage to users)."""

from __future__ import annotations

from enum import Enum


class AIProviderErrorCode(str, Enum):
    CONNECTION_FAILURE = "CONNECTION_FAILURE"
    TIMEOUT = "TIMEOUT"
    MODEL_UNAVAILABLE = "MODEL_UNAVAILABLE"
    INVALID_REQUEST = "INVALID_REQUEST"
    INVALID_PROVIDER_RESPONSE = "INVALID_PROVIDER_RESPONSE"
    MALFORMED_STRUCTURED_OUTPUT = "MALFORMED_STRUCTURED_OUTPUT"
    OUTPUT_TRUNCATION = "OUTPUT_TRUNCATION"
    STREAMING_INTERRUPTION = "STREAMING_INTERRUPTION"
    CANCELLED = "CANCELLED"
    CONCURRENCY_LIMIT = "CONCURRENCY_LIMIT"


class AIProviderError(Exception):
    def __init__(self, code: AIProviderErrorCode, message: str):
        self.code = code
        self.message = message
        super().__init__(message)

    def user_safe_dict(self) -> dict[str, str]:
        return {"error": self.code.value, "message": self.message}
