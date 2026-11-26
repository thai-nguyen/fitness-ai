"""Ollama HTTP adapter (backend-only; no Flutter direct access)."""

from __future__ import annotations

import asyncio
import json
import time
from collections.abc import AsyncIterator
from typing import Any

import httpx

from app.core.config import Settings
from app.modules.ai_coach.providers.contracts import (
    AIMessage,
    AIProviderCapabilities,
    AIRequest,
    AIResponse,
    AIStreamEvent,
    AIStructuredRequest,
    AIUsage,
)
from app.modules.ai_coach.providers.errors import AIProviderError, AIProviderErrorCode


def _messages_to_ollama(messages: tuple[AIMessage, ...]) -> list[dict[str, str]]:
    return [{"role": m.role.value, "content": m.content} for m in messages]


class OllamaProvider:
    def __init__(self, settings: Settings, client: httpx.AsyncClient | None = None):
        self._settings = settings
        self._client = client
        self._owns_client = client is None
        self._sem = asyncio.Semaphore(max(1, settings.ai_max_concurrent_requests))
        self.name = "ollama"

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            timeout = httpx.Timeout(
                connect=self._settings.ai_connect_timeout_seconds,
                read=self._settings.ai_read_timeout_seconds,
                write=self._settings.ai_connect_timeout_seconds,
                pool=self._settings.ai_connect_timeout_seconds,
            )
            self._client = httpx.AsyncClient(
                base_url=self._settings.ollama_base_url,
                timeout=timeout,
            )
        return self._client

    async def aclose(self) -> None:
        if self._owns_client and self._client is not None:
            await self._client.aclose()
            self._client = None

    async def capabilities(self) -> AIProviderCapabilities:
        client = await self._get_client()
        try:
            resp = await client.get("/api/tags")
            resp.raise_for_status()
            payload = resp.json()
        except httpx.ConnectError as exc:
            raise AIProviderError(
                AIProviderErrorCode.CONNECTION_FAILURE, "AI provider unavailable"
            ) from exc
        except httpx.TimeoutException as exc:
            raise AIProviderError(AIProviderErrorCode.TIMEOUT, "AI provider timeout") from exc
        except Exception as exc:
            raise AIProviderError(
                AIProviderErrorCode.INVALID_PROVIDER_RESPONSE, "invalid provider response"
            ) from exc

        models = payload.get("models") or []
        match = next(
            (m for m in models if m.get("name") == self._settings.ollama_model),
            None,
        )
        if match is None:
            raise AIProviderError(
                AIProviderErrorCode.MODEL_UNAVAILABLE,
                "configured model not available",
            )
        details = match.get("details") or {}
        caps = match.get("capabilities") or []
        return AIProviderCapabilities(
            chat=True,
            structured_json=True,  # evaluated via /api/chat format=json
            streaming=True,
            tools="tools" in caps,
            thinking="thinking" in caps,
            model_tag=match.get("name") or self._settings.ollama_model,
            model_digest=match.get("digest"),
            quantization=details.get("quantization_level"),
            context_length=details.get("context_length"),
            notes=tuple(str(c) for c in caps),
        )

    async def _chat_once(
        self,
        request: AIRequest,
        *,
        force_json: bool,
        stream: bool = False,
    ) -> AIResponse:
        if not self._sem._value and self._sem.locked():  # noqa: SLF001
            # best-effort concurrency signal when saturated
            pass
        try:
            await asyncio.wait_for(self._sem.acquire(), timeout=0.01)
        except TimeoutError as exc:
            raise AIProviderError(
                AIProviderErrorCode.CONCURRENCY_LIMIT, "AI concurrency limit reached"
            ) from exc

        client = await self._get_client()
        body: dict[str, Any] = {
            "model": self._settings.ollama_model,
            "messages": _messages_to_ollama(request.messages),
            "stream": stream,
            "options": {
                "temperature": request.temperature,
                "num_predict": request.max_tokens,
            },
        }
        if force_json:
            body["format"] = "json"
        # Prefer not to expose thinking traces
        body["think"] = False

        t0 = time.perf_counter()
        try:
            resp = await asyncio.wait_for(
                client.post("/api/chat", json=body),
                timeout=self._settings.ai_total_timeout_seconds,
            )
        except httpx.ConnectError as exc:
            raise AIProviderError(
                AIProviderErrorCode.CONNECTION_FAILURE, "AI provider unavailable"
            ) from exc
        except (httpx.TimeoutException, TimeoutError) as exc:
            raise AIProviderError(AIProviderErrorCode.TIMEOUT, "AI provider timeout") from exc
        finally:
            self._sem.release()

        if resp.status_code == 404:
            raise AIProviderError(
                AIProviderErrorCode.MODEL_UNAVAILABLE, "configured model not available"
            )
        if resp.status_code >= 400:
            raise AIProviderError(
                AIProviderErrorCode.INVALID_REQUEST, "invalid AI provider request"
            )
        try:
            data = resp.json()
        except json.JSONDecodeError as exc:
            raise AIProviderError(
                AIProviderErrorCode.INVALID_PROVIDER_RESPONSE, "invalid provider response"
            ) from exc

        message = (data.get("message") or {}).get("content") or ""
        # Strip accidental thinking if present in alternate fields
        if not message and (data.get("message") or {}).get("thinking"):
            raise AIProviderError(
                AIProviderErrorCode.INVALID_PROVIDER_RESPONSE,
                "provider returned thinking without content",
            )
        eval_count = data.get("eval_count")
        prompt_eval = data.get("prompt_eval_count")
        usage = AIUsage(
            prompt_tokens=prompt_eval if isinstance(prompt_eval, int) else None,
            completion_tokens=eval_count if isinstance(eval_count, int) else None,
            total_tokens=(
                (prompt_eval or 0) + (eval_count or 0)
                if isinstance(prompt_eval, int) or isinstance(eval_count, int)
                else None
            ),
        )
        latency_ms = (time.perf_counter() - t0) * 1000
        return AIResponse(
            text=message,
            usage=usage,
            raw_meta={
                "done": data.get("done"),
                "done_reason": data.get("done_reason"),
                "model": data.get("model"),
            },
            latency_ms=latency_ms,
            ttft_ms=None,  # non-stream path; streaming measures TTFT
        )

    async def chat(self, request: AIRequest) -> AIResponse:
        return await self._chat_once(request, force_json=False)

    async def structured(self, request: AIStructuredRequest) -> AIResponse:
        response = await self._chat_once(request, force_json=request.force_json)
        text = response.text.strip()
        if not text:
            raise AIProviderError(
                AIProviderErrorCode.MALFORMED_STRUCTURED_OUTPUT, "empty structured output"
            )
        try:
            json.loads(text)
        except json.JSONDecodeError as exc:
            raise AIProviderError(
                AIProviderErrorCode.MALFORMED_STRUCTURED_OUTPUT,
                "structured output is not valid JSON",
            ) from exc
        if response.raw_meta.get("done_reason") == "length":
            raise AIProviderError(
                AIProviderErrorCode.OUTPUT_TRUNCATION, "structured output truncated"
            )
        return response

    async def stream(self, request: AIRequest) -> AsyncIterator[AIStreamEvent]:
        client = await self._get_client()
        body = {
            "model": self._settings.ollama_model,
            "messages": _messages_to_ollama(request.messages),
            "stream": True,
            "think": False,
            "options": {
                "temperature": request.temperature,
                "num_predict": request.max_tokens,
            },
        }
        seq = 0
        yield AIStreamEvent("started", {"request_id": request.request_id}, seq)
        seq += 1
        t0 = time.perf_counter()
        ttft_ms: float | None = None
        assembled: list[str] = []
        try:
            async with client.stream("POST", "/api/chat", json=body) as resp:
                if resp.status_code >= 400:
                    yield AIStreamEvent(
                        "error",
                        {"error": AIProviderErrorCode.INVALID_REQUEST.value},
                        seq,
                    )
                    return
                async for line in resp.aiter_lines():
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                    except json.JSONDecodeError:
                        yield AIStreamEvent(
                            "error",
                            {"error": AIProviderErrorCode.INVALID_PROVIDER_RESPONSE.value},
                            seq,
                        )
                        return
                    piece = ((data.get("message") or {}).get("content")) or ""
                    if piece:
                        if ttft_ms is None:
                            ttft_ms = (time.perf_counter() - t0) * 1000
                        assembled.append(piece)
                        yield AIStreamEvent("text_delta", {"text": piece}, seq)
                        seq += 1
                    if data.get("done"):
                        yield AIStreamEvent(
                            "completed",
                            {
                                "text": "".join(assembled),
                                "ttft_ms": ttft_ms,
                                "latency_ms": (time.perf_counter() - t0) * 1000,
                            },
                            seq,
                        )
                        return
        except httpx.ConnectError as exc:
            raise AIProviderError(
                AIProviderErrorCode.CONNECTION_FAILURE, "AI provider unavailable"
            ) from exc
        except httpx.TimeoutException as exc:
            raise AIProviderError(AIProviderErrorCode.TIMEOUT, "AI provider timeout") from exc
        yield AIStreamEvent(
            "error",
            {"error": AIProviderErrorCode.STREAMING_INTERRUPTION.value},
            seq,
        )
