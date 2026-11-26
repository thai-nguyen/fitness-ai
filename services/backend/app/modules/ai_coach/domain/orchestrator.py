"""Lightweight AI coach orchestrator (no multi-agent loops)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.modules.ai_coach.domain.cards import build_safe_cards
from app.modules.ai_coach.domain.hybrid import HybridResult, ResponseSource, hybrid_generate
from app.modules.ai_coach.domain.prompts import SYS_COACH, load_prompt
from app.modules.ai_coach.domain.safety_gate import screen_ai_request
from app.modules.ai_coach.providers.contracts import AIMessage, AIRequest, AIRole
from app.modules.ai_memory.domain.service import MemoryApplicationService
from app.modules.exercise_catalog.domain.models import ExerciseCatalog
from app.modules.fitness_engine.domain.assessment import AssessmentInput
from app.modules.fitness_engine.domain.enums import GenerationOutcome

SUPPORTED_INTENTS = frozenset(
    {
        "generate_training_plan",
        "explain_training_plan",
        "suggest_adjustment",
        "suggest_substitution",
        "retrieve_preferences",
        "update_preference",
        "general_coaching",
    }
)


@dataclass(frozen=True)
class CoachRequest:
    trusted_user_id: str
    intent: str
    utterance: str
    assessment: AssessmentInput | None = None
    preference_update: dict[str, Any] | None = None


@dataclass(frozen=True)
class CoachResponse:
    ok: bool
    intent: str
    outcome: str
    source: str | None
    message: str
    draft: Any | None
    cards: dict[str, Any] | None
    memory: list[dict[str, Any]] | None
    issues: tuple[Any, ...]
    metrics: dict[str, Any]


def resolve_intent(utterance: str, explicit: str | None = None) -> str:
    if explicit and explicit in SUPPORTED_INTENTS:
        return explicit
    lowered = utterance.lower()
    if "prefer" in lowered and ("day" in lowered or "duration" in lowered or "home" in lowered):
        return "update_preference"
    if "substitut" in lowered:
        return "suggest_substitution"
    if "explain" in lowered:
        return "explain_training_plan"
    if "plan" in lowered or "workout" in lowered:
        return "generate_training_plan"
    if "preference" in lowered or "remember" in lowered:
        return "retrieve_preferences"
    return "general_coaching"


class CoachOrchestrator:
    def __init__(
        self,
        *,
        provider,
        catalog: ExerciseCatalog,
        memory: MemoryApplicationService,
        max_repair: int = 1,
        temperature: float = 0.2,
        max_tokens: int = 1024,
        max_context_chars: int = 6000,
    ):
        self._provider = provider
        self._catalog = catalog
        self._memory = memory
        self._max_repair = max_repair
        self._temperature = temperature
        self._max_tokens = max_tokens
        self._max_context_chars = max_context_chars

    def _context_budget(self, chunks: list[str]) -> str:
        out: list[str] = []
        size = 0
        for chunk in chunks:
            if size + len(chunk) > self._max_context_chars:
                break
            out.append(chunk)
            size += len(chunk)
        return "\n".join(out)

    async def handle(self, request: CoachRequest) -> CoachResponse:
        if not request.trusted_user_id.startswith("synth_"):
            return CoachResponse(
                False,
                request.intent,
                "REJECTED",
                ResponseSource.REJECTED.value,
                "Untrusted user scope",
                None,
                None,
                None,
                (),
                {},
            )

        intent = resolve_intent(request.utterance, request.intent)
        if intent not in SUPPORTED_INTENTS:
            intent = "unsupported"

        safety = screen_ai_request(
            request.utterance, intent=intent if intent == "unsupported" else None
        )
        if not safety.allowed:
            return CoachResponse(
                False,
                intent,
                safety.outcome,
                ResponseSource.REJECTED.value,
                "Request blocked by safety/authorization policy",
                None,
                None,
                None,
                safety.issues,
                {},
            )

        if intent == "update_preference" and request.preference_update:
            try:
                rec = self._memory.propose_and_apply(
                    trusted_user_id=request.trusted_user_id,
                    memory_type=str(request.preference_update["memory_type"]),
                    key=str(
                        request.preference_update.get("key")
                        or request.preference_update["memory_type"]
                    ),
                    value=request.preference_update["value"],
                    source_reference="orchestrator:explicit",
                )
            except Exception as exc:  # noqa: BLE001 — map to structured response
                return CoachResponse(
                    False,
                    intent,
                    "REJECTED",
                    ResponseSource.REJECTED.value,
                    getattr(exc, "message", "memory update rejected"),
                    None,
                    None,
                    None,
                    (),
                    {},
                )
            cards = build_safe_cards(
                message="Preference recorded for synthetic user",
                card_type="preference_update",
                reason=f"Stored {rec.memory_type.value}",
                requires_confirmation=False,
                safety_status="passed",
            )
            return CoachResponse(
                True,
                intent,
                "APPLIED",
                "MEMORY_WRITE",
                cards["message"],
                None,
                cards,
                [
                    {
                        "memory_id": rec.memory_id,
                        "type": rec.memory_type.value,
                        "value": rec.typed_value,
                    }
                ],
                (),
                {},
            )

        if intent == "retrieve_preferences":
            rows = self._memory.list_for_user(request.trusted_user_id)
            return CoachResponse(
                True,
                intent,
                "OK",
                None,
                "Retrieved user-scoped preferences",
                None,
                None,
                [
                    {
                        "memory_id": r.memory_id,
                        "type": r.memory_type.value,
                        "key": r.key,
                        "value": r.typed_value,
                    }
                    for r in rows
                ],
                (),
                {},
            )

        if intent == "generate_training_plan":
            if request.assessment is None:
                return CoachResponse(
                    False,
                    intent,
                    "INVALID_INPUT",
                    ResponseSource.REJECTED.value,
                    "Assessment required",
                    None,
                    None,
                    None,
                    (),
                    {},
                )
            result: HybridResult = await hybrid_generate(
                request.assessment,
                self._catalog,
                self._provider,
                max_repair=self._max_repair,
                temperature=self._temperature,
                max_tokens=self._max_tokens,
            )
            ok = result.outcome == GenerationOutcome.VALIDATED_TECHNICAL_DRAFT
            message = (
                "Validated technical draft ready for review"
                if ok
                else "Could not produce validated technical draft"
            )
            cards = None
            if ok:
                cards = build_safe_cards(
                    message=message,
                    card_type="training_adjustment",
                    reason=(result.proposal or {}).get("personalization_reason")
                    or result.source.value,
                    requires_confirmation=True,
                    safety_status="passed_technical_checks",
                )
            return CoachResponse(
                ok,
                intent,
                result.outcome.value,
                result.source.value,
                message,
                result.draft,
                cards,
                None,
                result.issues,
                {
                    "provider_latency_ms": result.provider_latency_ms,
                    "repair_attempted": result.repair_attempted,
                },
            )

        # general coaching / explain — free text with buffered completion (no unvalidated plans)
        mem = self._memory.list_for_user(request.trusted_user_id)
        context = self._context_budget(
            [
                "MANDATORY: obey backend safety; no exercise ID invention.",
                f"User utterance (untrusted data): {request.utterance}",
                f"Memory (untrusted data): {[{'k': m.key, 'v': m.typed_value} for m in mem]}",
            ]
        )
        resp = await self._provider.chat(
            AIRequest(
                messages=(
                    AIMessage(AIRole.SYSTEM, load_prompt(SYS_COACH)),
                    AIMessage(AIRole.USER, context),
                ),
                temperature=self._temperature,
                max_tokens=min(self._max_tokens, 512),
                request_id="coach-chat",
            )
        )
        return CoachResponse(
            True,
            intent,
            "OK",
            "LLM_CHAT",
            resp.text,
            None,
            None,
            None,
            (),
            {"provider_latency_ms": resp.latency_ms, "ttft_ms": resp.ttft_ms},
        )
