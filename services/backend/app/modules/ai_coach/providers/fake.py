"""Deterministic fake provider for unit/integration tests (no network)."""

from __future__ import annotations

import json
from collections.abc import AsyncIterator
from dataclasses import dataclass, field

from app.modules.ai_coach.providers.contracts import (
    AIProviderCapabilities,
    AIRequest,
    AIResponse,
    AIStreamEvent,
    AIStructuredRequest,
    AIUsage,
)
from app.modules.ai_coach.providers.errors import AIProviderError, AIProviderErrorCode


@dataclass
class FakeAIProvider:
    name: str = "fake"
    structured_payload: dict = field(default_factory=dict)
    chat_text: str = "Synthetic coaching reply."
    fail_code: AIProviderErrorCode | None = None
    stream_chunks: tuple[str, ...] = ("Synthetic ", "stream ", "reply.")

    async def capabilities(self) -> AIProviderCapabilities:
        return AIProviderCapabilities(
            chat=True,
            structured_json=True,
            streaming=True,
            tools=False,
            thinking=False,
            model_tag="fake-model",
            notes=("deterministic test double",),
        )

    async def chat(self, request: AIRequest) -> AIResponse:
        if self.fail_code:
            raise AIProviderError(self.fail_code, "fake failure")
        return AIResponse(
            text=self.chat_text,
            usage=AIUsage(prompt_tokens=10, completion_tokens=5, total_tokens=15),
            latency_ms=1.0,
            ttft_ms=0.5,
        )

    async def structured(self, request: AIStructuredRequest) -> AIResponse:
        if self.fail_code:
            raise AIProviderError(self.fail_code, "fake failure")
        return AIResponse(
            text=json.dumps(self.structured_payload),
            usage=AIUsage(prompt_tokens=20, completion_tokens=10, total_tokens=30),
            latency_ms=1.5,
            ttft_ms=0.7,
        )

    async def stream(self, request: AIRequest) -> AsyncIterator[AIStreamEvent]:
        if self.fail_code:
            raise AIProviderError(self.fail_code, "fake failure")
        yield AIStreamEvent("started", {"request_id": request.request_id}, 0)
        seq = 1
        for chunk in self.stream_chunks:
            yield AIStreamEvent("text_delta", {"text": chunk}, seq)
            seq += 1
        yield AIStreamEvent("completed", {"text": "".join(self.stream_chunks)}, seq)
