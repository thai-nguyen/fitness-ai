# ADR-0012 — AI Provider Abstraction

| Field | Value |
| --- | --- |
| Status | `ACCEPTED` (architectural direction + Phase 0 Ollama binding via ADR-0017); unused provider methods / chat orchestration remain PENDING M05 |
| Date | 2026-11-25 |
| Updated | 2026-11-25 (Zero-Cost / Ollama directive) |

## Context

Need swappable LLM backends without coupling domain/orchestrator to a vendor. PO zero-cost constraint selects Ollama for Phase 0 (ADR-0017).

## Decision

1. All LLM access goes through an **LLM Gateway + Provider Adapter** interface.
2. **OllamaProviderAdapter** is the **only** adapter to implement for Phase 0 POCs / development.
3. Do **not** implement paid cloud adapters (OpenAI/Anthropic/Gemini/etc.) without PO approval.
4. Configuration: `OLLAMA_BASE_URL`, `OLLAMA_MODEL` (names illustrative) via environment — **no hardcoded LAN IPs** in source.
5. Abstraction remains for future extensibility after PO approval of any new provider.

## Alternatives

Hard-code Ollama HTTP in orchestrator — rejected. Ship paid SDKs now — rejected (ADR-0017).

## Consequences

M05 validates Ollama/Qwen capabilities. If insufficient, evaluate other **zero-cost** options before paid proposals.

## Validation

PH00-M05 adapter + model evaluation matrix (ADR-0017).

## Related

ADR-0017, CR-20261125, `AI_ARCHITECTURE.md`.

## Approval scope (2026-11-25)

**Accepted:** architectural principle / direction only (Tech Lead + Project Owner).
**Not accepted as proven:** feasibility, schemas, algorithms, or production readiness � remain PENDING for the validation milestones named in this ADR.
