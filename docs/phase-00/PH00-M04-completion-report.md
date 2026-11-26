# PH00-M04 Completion Report — Fitness Engine Feasibility

| Field | Value |
| --- | --- |
| Milestone | PH00-M04 — Fitness Engine & Content Feasibility |
| Status | **`ACCEPTED`** (technical feasibility; D-029) — provisional rules remain non-expert-approved |
| Date | 2026-11-26 |
| Authorization | D-021/D-029; M04 local commit authorized; push **NO-GO** |
| Related backlog | PH00-TB-012 `ACCEPTED`; PH00-TB-013 `ACCEPTED` (assessment scope); OI-003/OI-005 open |
| TL review | **PASS WITH CONDITIONS** remediated — [`PH00-M04-remediation-report.md`](PH00-M04-remediation-report.md) |
| Evaluation runner | `scripts/run_m04_evaluation.py` → [`m04-evaluation-report.json`](m04-evaluation-report.json) |

## 1. Executive summary

PH00-M03 was closed **ACCEPTED WITH WAIVER** and locally committed. PH00-M04 delivers a **pure-domain deterministic fitness engine** (no LLM/Ollama/paid APIs/RAG/Postgres required for engine tests): assessment contract, fixture exercise catalog, provisional rule catalog, templates, schedule/volume/intensity/duration, safety screening, substitution, independent validator, generator pipeline, ≥30 synthetic scenarios, and documentation. Provisional rules are **not** expert-approved. M05 remains **NO-GO**.

## 2. M03 acceptance and waiver record

- Status: **`ACCEPTED` WITH WAIVER** (canonical status `ACCEPTED`; qualifier WITH WAIVER).
- Decision: **D-020**; Change request: [`CR-20261125-B`](../change-requests/CR-20261125-m03-retry-waiver.md).
- F-M03-001 interactive Retry Recovery: **not** PASS/VERIFIED; future regression still required (**OI-013**).
- F-M03-002 accepted; F-M03-003 accepted with limitations (**OI-016**); F-M03-004 license PENDING (**OI-014**); F-M03-005 static CI accepted, hosted **NOT_EXECUTED** (**OI-015**); vuln scan pending (**OI-017**).

## 3. M03 local commit SHA

`a99ad5ef7aced1e4c4fa970d314fa3048dc84885` — `feat: establish engineering foundation and close PH00-M03`

## 4. M04 authorized scope

Deterministic fitness-engine technical feasibility only. No production plan activation, no public generation API, no Ollama inference, no paid services, no M05.

## 5. Actual technical backlog IDs

| ID | Status |
| --- | --- |
| PH00-TB-012 | `VALIDATED` (engineering; TL accept PENDING; expert rules OI-003) |
| PH00-TB-013 | `IMPLEMENTED` (assessment done; production content OI-005; app LICENSE OI-014) |

## 6–7. Domain architecture & implementation structure

Modular monolith preserved. Pure domain under:

```text
services/backend/app/modules/
  exercise_catalog/domain/   # models, validation, fixtures
  fitness_engine/domain/     # assessment → generator pipeline
```

No FastAPI/SQLAlchemy/HTTP/Ollama dependency inside engine domain.

## 8. Fitness business rules inventory

Authoritative: [`../business-rules/FITNESS_BUSINESS_RULES_M04.md`](../business-rules/FITNESS_BUSINESS_RULES_M04.md) + `rules.py` (`m04-provisional-1`). **Zero** rules marked `EXPERT_APPROVED`.

## 9–11. Exercise schema, catalog, provenance

See [`../architecture/EXERCISE_SCHEMA_AND_CATALOG_M04.md`](../architecture/EXERCISE_SCHEMA_AND_CATALOG_M04.md).

| Metric | Value |
| --- | --- |
| Catalog version | `fixture-v1` |
| Exercises | 26 (25 active + 1 inactive) |
| Catalog validation issues | 0 |
| Content | Original synthetic metadata only |
| External datasets | Not ingested (UNVERIFIED) |

## 12–19. Engine capabilities

| Capability | Module | Notes |
| --- | --- | --- |
| Selector | `selector.py` | Hard filters; stable `exercise_id` tie-break |
| Templates | `templates.py` | Beginner FB, general, home, gym strength |
| Schedule | `schedule.py` | Availability + preferred + soft spacing |
| Volume | `volume.py` | Sets; secondary @ 0.5; provisional weekly caps |
| Intensity | `intensity.py` | Rep range / RPE / rest — no absolute loads |
| Duration | `duration.py` | Estimate ≠ actual; must fit max minutes |
| Safety | `safety.py` | Technical screening; see SAFETY_POLICY_M04 |
| Substitution | `substitution.py` | Group-preferring; no clinical equivalence claim |
| Draft contract | `draft.py` | schema `1.0.0`; never activated |
| Validator | `validator.py` | Independent of generator |

## 20–22. Draft / validator / generation flow

Pipeline: validate assessment → safety → template → schedule → select → volume/intensity → duration → draft → independent validate → structured outcome.

## 23. Example synthetic input/output

Input: beginner `general_fitness`, bodyweight, Mon/Wed/Fri, 45 min, adult_eligible=true.

Typical outcome: `VALIDATED_TECHNICAL_DRAFT` with home/bodyweight-compatible template and eligible fixture IDs only (see unit tests).

## 24–27. Evaluation dataset & metrics (executed)

Command: `python -c` evaluation runner / `pytest tests/fitness_engine` (2026-11-26 local).

| Metric | Result |
| --- | --- |
| Scenario count | 32 |
| Positive pass rate | 10/10 (100%) |
| Negative pass rate | 15/15 (100%) |
| Boundary pass | 7/7 |
| Hard constraint compliance (dataset) | 100% |
| Unknown exercise IDs in validated drafts | 0 |
| Invalid drafts incorrectly accepted | 0 |
| Critical safety blocks missed | 0 |
| Determinism checks | Pass (unit + S-BND-005) |
| Latency sample n | 32 |
| Median latency | ~0.076 ms |
| p95 latency | ~0.186 ms |
| Max latency | ~0.358 ms |

Latency measured with `time.perf_counter` on local Windows; not a production SLA claim. No clinical effectiveness claimed.

## 28–29. Automated / foundation regression

| Check | Result |
| --- | --- |
| `pytest tests/fitness_engine` | **39 passed** (exit 0) |
| Fitness engine needs PG/API/Ollama | **No** |
| Full backend + local quality script | See §39 final validation below |
| Hosted GitHub Actions | **NOT_EXECUTED** (OI-015) |

## 30. Rule-to-test traceability

Rules reference `implementation_ref` / `test_ref` in `rules.py`. Scenario expected rule IDs in `evaluation.py`. Docs: business-rules catalog.

## 31. Expert review requirements

All provisional/expert-required rules + production catalog content remain pending (OI-003, OI-005). Do not release provisional recommendations to real users.

## 32. Zero-Cost First compliance

No new paid services. No new runtime dependencies required for engine (stdlib + existing pytest/ruff). No Ollama inference executed.

## 33. Decisions without explicit PO guidance

D-022..D-028 recorded in Decision Register (rule representation, fixture format, tie-break, result types, duration assumptions, safety boundary, evaluation organization).

## 34. Files created or modified (primary)

- `services/backend/app/modules/exercise_catalog/**`
- `services/backend/app/modules/fitness_engine/**`
- `services/backend/tests/fitness_engine/**`
- `docs/business-rules/FITNESS_BUSINESS_RULES_M04.md`
- `docs/architecture/EXERCISE_SCHEMA_AND_CATALOG_M04.md`
- `docs/architecture/TRAINING_PLAN_DRAFT_CONTRACT_M04.md`
- `docs/architecture/SAFETY_POLICY_M04.md`
- `docs/architecture/FITNESS_ENGINE_ARCHITECTURE.md` (updated)
- `docs/phase-00/M04_EVALUATION_SCENARIOS.md`
- `docs/phase-00/execution-tracker.md` (incl. F-TRK remediation)
- `docs/baseline/OPEN_ISSUES.md` (OI-013..017)
- `docs/risks/RISK_REGISTER.md` (R-025/026 + refs)
- `docs/backlog/TECHNICAL_BACKLOG.md`
- `docs/baseline/DECISION_REGISTER.md` (D-022..028)
- This completion report

## 35. Backlog statuses

TB-012 `VALIDATED` (eng); TB-013 `IMPLEMENTED`; TB-011 LICENSE still blocked; M05 tasks untouched.

## 36. Remaining risks and blockers

OI-003 expert rules; OI-005 content licensing; OI-013..017 M03 follow-ups; R-003/R-004/R-025/R-026. M04 commit unauthorized until TL accept.

## 37. Acceptance checklist

| Criterion | Met? |
| --- | --- |
| M03 closure + local checkpoint | Yes |
| Architecture preserved (modular monolith) | Yes |
| Typed assessment / exercise schema | Yes |
| Fixture catalog | Yes (26) |
| Traceable rule catalog | Yes |
| Selector / templates / schedule / volume / intensity / duration | Yes |
| Safety / substitution / independent validator / generator | Yes |
| Structured failure outcomes | Yes |
| ≥30 synthetic scenarios + tests passing | Yes (32; 39 pytest) |
| No LLM / paid services | Yes |
| Provenance documented; expert gaps explicit | Yes |
| Foundation regression | See final validation |
| Completion report | Yes |
| Self-accept M04 | **No** |
| Commit/push M04 | **No** |

## 38. M05 readiness recommendation

**NO-GO** until Tech Lead accepts M04 and explicitly authorizes M05. Engine contracts are ready as deterministic boundary for future AI proposals.

## 39. Final Git working-tree status

Recorded at end of validation (uncommitted M04 work expected). **Do not commit/push** without authorization.

## 40. Tracker remediation evidence (F-TRK-001..005)

| Finding | Remediation |
| --- | --- |
| F-TRK-001 | Change log v2.0 entry added (M03 waiver D-020/CR-B, commit `a99ad5e`, M04 GO D-021, push NO-GO) |
| F-TRK-002 | M01 “Next milestone authorization PENDING” clarified as **historical snapshot**; M02 now ACCEPTED; current auth = M04 |
| F-TRK-003 | M06 depends on Flutter foundation from M03; **Drift not in M03** — Drift/local persistence required in M06 |
| F-TRK-004 | Status legend explains `ACCEPTED` WITH WAIVER semantics |
| F-TRK-005 | OI-013..017 (+ risk refs R-009/023/025/026) track Retry, LICENSE, hosted Actions, clean-env reproducibility, vuln scan |

## 41. Final validation commands (executed 2026-11-26)

| Command | Exit | Result |
| --- | --- | --- |
| `ruff check app tests` | 0 | All checks passed |
| `ruff format --check app tests` | 0 | 49 files already formatted |
| `pytest -q` (backend) | 0 | **48 passed** (includes 39 fitness_engine) |
| `.\scripts\local_quality.ps1` | 0 | Backend + Flutter analyze/tests + compose config OK |
| Hosted GitHub Actions | — | **NOT_EXECUTED** (OI-015) |
| Ollama inference | — | **Not executed** (M05 NO-GO) |

Mobile dart format touch-ups applied solely so the quality gate’s `--set-exit-if-changed` passes (no Flutter feature changes for M04).

### Final git status (summary)

- Branch: `main` (tracking `origin/main`); HEAD remains M03 checkpoint `a99ad5e…`
- Uncommitted: M04 domain/modules/tests/docs + incidental ruff/dart format on foundation files
- Untracked runtime evidence under `scripts/runtime-evidence/` — **do not commit** without review
- **M04 commit NOT AUTHORIZED; push NO-GO; M05 NO-GO; not self-accepted**

**STOP** — awaiting Tech Lead / Project Owner review of this report.
