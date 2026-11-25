# ADR-0017 — Zero-Cost First & Local AI First (Ollama)

| Field | Value |
| --- | --- |
| Status | `ACCEPTED` (development constraint + initial provider) |
| Date | 2026-11-25 |
| Decision register | D-010, D-011 |
| Related | ADR-0012, AUTH-003 (subsequent approved change), PH00-M02/M05 |
| Approver | Project Owner (explicit directive) |

## Context

- Consolidated Baseline (AUTH-003) historically mentioned an OpenAI adapter **candidate** subject to governance/POC.
- Project Owner established a **zero-cost development strategy**: prefer existing local hardware, open-source software, and free tooling.
- Existing local infrastructure: **Ollama** runtime with **Qwen 3.5 9B**, base URL reported as `http://192.168.8.54:11434` (LAN), AI API subscription cost = zero.
- Exact installed model tag and endpoint capabilities must be **verified** before implementation (not assumed).

## Decision

1. **Zero-Cost First:** No paid API, cloud infrastructure, SaaS subscription, or billable service may be introduced without **explicit Project Owner approval**.
2. **Local AI First:** Use **Ollama** as the **primary AI provider for development and Phase 0 POCs**.
3. Initial POC model target: **Qwen 3.5 9B** (exact tag TBD via verification).
4. Preserve **hybrid AI architecture** (orchestrator, context builder, structured memory, tool registry, Fitness Engine, safety guardrails, structured output validation, LLM gateway).
5. Implement an **Ollama Provider Adapter** behind the existing lightweight provider abstraction (ADR-0012).
6. **Do not** implement OpenAI, Anthropic, Gemini, or other **paid** cloud AI integrations unless PO later approves.
7. Keep Ollama **base URL** and **model name** configurable via **environment variables** — never hardcode LAN addresses in source.
8. **Do not** expose Ollama to the public internet or directly to mobile clients; all mobile AI traffic goes through the authenticated FastAPI backend.
9. **Model suitability and production readiness remain PENDING** until PH00-M05 (and related) validation — this ADR does **not** certify Qwen 3.5 9B for production quality, tool-calling, structured output, latency, or concurrency.

## Alternatives considered

| Alternative | Outcome |
| --- | --- |
| Paid cloud LLM now (e.g. OpenAI) | Rejected for development — conflicts with zero-cost constraint |
| Call Ollama directly from mobile | Rejected — security/trust boundary |
| Hardcode LAN IP in repo | Rejected — environment/config only |
| Skip provider abstraction | Rejected — future extensibility still required |

## Consequences

### Positive

- Zero AI API spend during Phase 0 POCs
- Data stays on LAN for development inference
- Aligns architecture with available hardware

### Risks / follow-ups

- Local hardware capacity (CPU/GPU/RAM) may limit concurrency
- Model may fail structured JSON / tool-calling — evaluate app-controlled routing before paid alternatives
- Free-tier GitHub Actions / other free tools may have limits — document before relying at scale
- Production hosting remains **PENDING**

### Supersession note

Does **not** silently rewrite AUTH-003 text. Recorded as **subsequent approved change** via Decision Register D-010/D-011 and [`../change-requests/CR-20261125-zero-cost-local-ai.md`](../change-requests/CR-20261125-zero-cost-local-ai.md). Historical OpenAI-candidate wording remains audit history; **execution direction for AI in Phase 0 is Ollama-first**.

## Validation requirements (PH00-M05+)

Verify model tag/endpoints; measure structured JSON, schema adherence, plan generation, exercise ID grounding, tool-calling or fallbacks, memory extraction, safety, VI/EN quality, latency, TPS, concurrency, resource use, timeouts. **No fabricated benchmarks.** If insufficient, report limitations and evaluate **zero-cost** alternatives before proposing paid services.

## Related product requirements

AI-001–013; AIR-001–012; Phase 0 AI POCs.
