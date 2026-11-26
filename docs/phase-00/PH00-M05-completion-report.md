# PH00-M05 Completion Report — AI Technical POCs

| Field | Value |
| --- | --- |
| Milestone | PH00-M05 — AI Technical POCs |
| Status | `VALIDATED` (engineering evidence) — **not self-accepted** |
| Date | 2026-11-26 |
| M04 commit | `a7a870a00cb018a22edcbd2500311e9fc1155672` |
| M05 commit | **NOT AUTHORIZED** |
| Push / M06+ / paid AI | **NO-GO** |

## 1. Executive summary

PH00-M04 was **ACCEPTED** for technical feasibility and locally committed. PH00-M05 demonstrates Hybrid AI feasibility against local **Ollama / qwen3.5:9b** with synthetic data: provider abstraction, structured JSON generation, template-first hybrid personalization validated by M04 engine, bounded repair + deterministic fallback, structured memory POC (in-memory + PostgreSQL table), safety/injection gates, streaming smoke, and reproducible evaluation. Live hybrid scenarios returned `LLM_PERSONALIZED` with **0** unknown exercise IDs. Provisional fitness rules remain non-expert-approved. M05 is **not** production AI Coach readiness.

## 2. M04 acceptance and local commit

- Acceptance: technical feasibility **ACCEPTED** (D-029); OI-003/005/013–017 preserved.
- SHA: `a7a870a00cb018a22edcbd2500311e9fc1155672`
- Message: `feat: establish deterministic fitness engine and close PH00-M04`

## 3. M05 authorization

D-030: M05 GO after M04 checkpoint; Ollama synthetic inference authorized; M05 commit NOT AUTHORIZED; push NO-GO; paid NO-GO.

## 4. Backlog / POC IDs

| ID | Status |
| --- | --- |
| PH00-TB-014 | `VALIDATED` (engineering; TL accept PENDING) |
| PH00-TB-015+ | untouched / NO-GO |

## 5–6. Architecture / structure

```text
services/backend/app/modules/ai_coach/   # providers, orchestrator, hybrid, safety, eval
services/backend/app/modules/ai_memory/  # structured memory service + SQL model
ai/prompts/                              # versioned prompts
scripts/run_m05_evaluation.py
alembic 20261126_0002 synthetic_ai_memory
```

Modular monolith preserved. No microservices / LangChain / vector DB / Redis.

## 7–8. Ollama environment & model identity

| Field | Value |
| --- | --- |
| Endpoint | Local LAN via process env `OLLAMA_BASE_URL` (not committed) |
| Model tag | `qwen3.5:9b` |
| Digest | `56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90` |
| Quantization | Q4_K_M |
| Context length (reported) | 262144 |
| Capabilities | completion, vision, tools, thinking (thinking disabled in requests) |

Committed defaults remain loopback placeholders. LAN IP supplied only through local env for live runs.

## 9–11. Provider abstraction / failures / orchestrator

See `docs/architecture/AI_PROVIDER_M05.md`, `AI_ORCHESTRATOR_M05.md`.

Error codes: CONNECTION_FAILURE, TIMEOUT, MODEL_UNAVAILABLE, INVALID_REQUEST, INVALID_PROVIDER_RESPONSE, MALFORMED_STRUCTURED_OUTPUT, OUTPUT_TRUNCATION, STREAMING_INTERRUPTION, CANCELLED, CONCURRENCY_LIMIT.

## 12–16. Prompts, structured generation, hybrid, M04 validation, repair

- Prompts: `ai/prompts/` (SYS-COACH-001, GEN-PERSONALIZE-001).
- Structured approach: Ollama `format=json` + allowlisted candidate IDs (Strategy C).
- Backend builds authoritative draft metadata; independent `validate_draft` + duration recalculation retained.
- Repair: max 1 attempt (`AI_MAX_REPAIR_ATTEMPTS`); then deterministic fallback (not counted as LLM success).
- Sources: `LLM_PERSONALIZED` / `LLM_REPAIRED` / `DETERMINISTIC_FALLBACK` / `REJECTED` / `REVIEW_REQUIRED`.

## 17–21. Memory

- Allowlisted preference types only; `synth_*` users only.
- Authoritative domain overrides memory; safety keys forbidden.
- In-memory service for unit tests; PostgreSQL `synthetic_ai_memory` via Alembic `20261126_0002`.
- Integration test: write → new engine/session read → cross-user miss → delete.

## 22–24. Context / cards / streaming

- Context builder truncates optional chunks; mandatory safety lines first.
- Cards/actions allowlisted; confirmation required for plan proposals; no activation.
- Streaming: started/text_delta/completed/error; TTFT measured on first content token; no thinking traces; plans not streamed unvalidated.

## 25–26. Safety / unauthorized actions

Deterministic gate blocks injection, cross-user access attempts, plan activation requests, SQL/URL exfil patterns, and concerning medical phrasing (REVIEW_REQUIRED). Evaluated in fake suite (`M05-SAFE-*`).

## 27–32. Evaluation results

### Fake-provider suite (mandatory CI-safe)

```text
services/backend/.venv/Scripts/python.exe scripts/run_m05_evaluation.py --mode fake --json docs/phase-00/m05-evaluation-report.json
```

| Metric | Result |
| --- | --- |
| Scenarios | **54/54** pass |
| Unknown IDs in validated drafts | 0 |
| Cross-user leak tests | pass |
| Paid external AI | 0 |

### Live smoke (executed with LAN env)

| Metric | Result |
| --- | --- |
| Chat latency | ~7501 ms (includes warm/cold variance) |
| Structured JSON | `{"status":"ok","n":1}` in ~317 ms |
| Stream TTFT | ~125 ms |
| Prompt/completion tokens (chat) | 23 / 2 |

Artifact: `docs/phase-00/m05-live-smoke.json`

### Live hybrid eval (n=2 bounded)

| Scenario | Outcome | Source | Unknown IDs | Provider latency |
| --- | --- | --- | --- | --- |
| M05-LIVE-01 | VALIDATED_TECHNICAL_DRAFT | LLM_PERSONALIZED | 0 | ~4009 ms |
| M05-LIVE-02 | VALIDATED_TECHNICAL_DRAFT | LLM_PERSONALIZED | 0 | ~4617 ms |

Artifact: `docs/phase-00/m05-live-eval.json`

### Strategy note

- A Deterministic baseline: covered in fake suite / M04 engine.
- C Hybrid template-first: live + fake validated.
- B Direct LLM full draft: **not** adopted as architecture; experimental comparison deferred beyond bounded hybrid (Hybrid remains authorized path).

## 33–35. Performance / cost

| Item | Actual |
| --- | --- |
| External API spend | **$0** |
| New paid infra | **$0** |
| Electricity/hardware cost | unknown / excluded |
| Live concurrency | 1 |
| TTFT target ≤3s | met on smoke stream (~0.13s); chat e2e can exceed 3s depending on cold start |

## 36. Data governance

Synthetic only. No real PHI. Thinking not persisted. Full prompts not logged by default. LAN ≠ privacy guarantee. Production governance remains M08 (OI-004).

## 37–38. Automated tests / M04 regression

| Check | Result |
| --- | --- |
| `pytest -q` | **100 passed** |
| `local_quality.ps1` | exit **0** |
| M04 eval runner | 32/32 (re-run at M05 close) |
| Hosted Actions | NOT_EXECUTED |

## 39. Reproduction commands

```powershell
# Fake (no network)
services\backend\.venv\Scripts\python.exe scripts\run_m05_evaluation.py --mode fake --json docs\phase-00\m05-evaluation-report.json

# Live (set LAN in process env; do not commit)
$env:OLLAMA_BASE_URL='http://<LAN-HOST>:11434'
$env:OLLAMA_MODEL='qwen3.5:9b'
services\backend\.venv\Scripts\python.exe scripts\run_m05_evaluation.py --mode live-smoke --json docs\phase-00\m05-live-smoke.json
services\backend\.venv\Scripts\python.exe scripts\run_m05_evaluation.py --mode live-eval --json docs\phase-00\m05-live-eval.json
```

## 40. Decisions without explicit PO detail

| ID | Decision |
| --- | --- |
| D-031 | Structured output via Ollama `format=json` + candidate allowlist |
| D-032 | Max 1 repair then deterministic fallback |
| D-033 | `synthetic_ai_memory` minimal PG table for POC |
| D-034 | Thinking disabled; never user-facing / never persisted |
| D-035 | Live tests require explicit runner mode + env (not default unit tests) |

## 41–42. Files / backlog

Primary adds under `ai_coach`, `ai_memory`, `ai/prompts`, `scripts/run_m05_evaluation.py`, Alembic `20261126_0002`, docs/architecture AI_* M05, this report + JSON artifacts.

TB-014 → `VALIDATED` (eng).

## 43. Risks / blockers

- Expert fitness approval still OI-003.
- Content licensing OI-005; LICENSE OI-014.
- Chat e2e latency can exceed 3s on cold/warm variance — performance target conditional.
- Tool-calling capability present but **not** required; app-controlled services used instead.
- Hosted CI cannot reach private LAN Ollama (by design).

## 44. Acceptance checklist

| Criterion | Met? |
| --- | --- |
| M04 closed + local commit | Yes |
| Ollama connectivity + exact model identity | Yes (live smoke) |
| Provider abstraction + fake provider | Yes |
| Structured generation | Yes |
| Hybrid + M04 validation | Yes |
| Repair + fallback | Yes |
| Memory + isolation + SQL persistence | Yes |
| Safety/injection evaluation | Yes (fake suite) |
| Streaming + TTFT | Yes (smoke) |
| ≥50 scenarios fake suite | Yes (54) |
| Zero paid AI | Yes |
| Self-accept / commit M05 | **No** |

## 45. Model suitability recommendation

**CONDITIONAL GO** for continued Phase 0 Hybrid AI POCs on local `qwen3.5:9b`: structured candidate selection worked in live hybrid samples with independent validation. **Not** suitable to claim production coaching quality, clinical safety, or expert-approved programming. Performance targets for interactive chat need further warm-path characterization.

## 46. M06 readiness

**NO-GO** until Tech Lead accepts M05 and PO authorizes M06. Drift/offline remains M06 scope.

## 47. Final Git status

| Field | Value |
| --- | --- |
| Branch | `main` |
| HEAD | `a7a870a00cb018a22edcbd2500311e9fc1155672` (M04) |
| vs origin | ahead 1 |
| M05 work | **uncommitted** (modified + untracked) |
| Exclude from any future commit | `scripts/runtime-evidence/`, `.env`, credentials, build outputs |
| Push | **NO-GO** |

Decisions recorded without waiting for additional PO guidance for M05 technical knobs: D-031–D-035.

**STOP** — awaiting independent Tech Lead review and explicit Project Owner authorization. Do not commit M05, push, or start M06.
