"""Minimal AI provider contracts for PH00-M05."""

from __future__ import annotations

from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol


class AIRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass(frozen=True)
class AIMessage:
    role: AIRole
    content: str


@dataclass(frozen=True)
class AIUsage:
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None


@dataclass(frozen=True)
class AIProviderCapabilities:
    chat: bool = True
    structured_json: bool = False
    streaming: bool = False
    tools: bool = False
    thinking: bool = False
    model_tag: str = ""
    model_digest: str | None = None
    quantization: str | None = None
    context_length: int | None = None
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class AIRequest:
    messages: tuple[AIMessage, ...]
    temperature: float = 0.2
    max_tokens: int = 1024
    request_id: str = "synthetic"


@dataclass(frozen=True)
class AIStructuredRequest(AIRequest):
    json_schema_hint: dict[str, Any] | None = None
    force_json: bool = True


@dataclass(frozen=True)
class AIResponse:
    text: str
    usage: AIUsage = field(default_factory=AIUsage)
    raw_meta: dict[str, Any] = field(default_factory=dict)
    latency_ms: float = 0.0
    ttft_ms: float | None = None


@dataclass(frozen=True)
class AIStreamEvent:
    event_type: str  # started|text_delta|progress|proposal_ready|completed|error
    data: dict[str, Any]
    sequence: int


class AIProvider(Protocol):
    @property
    def name(self) -> str: ...

    async def capabilities(self) -> AIProviderCapabilities: ...

    async def chat(self, request: AIRequest) -> AIResponse: ...

    async def structured(self, request: AIStructuredRequest) -> AIResponse: ...

    def stream(self, request: AIRequest) -> AsyncIterator[AIStreamEvent]: ...
