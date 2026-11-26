# PH00-M04 Remediation Report — Tech Lead PASS WITH CONDITIONS

| Field | Value |
| --- | --- |
| Milestone | PH00-M04 |
| Review decision | **PASS WITH CONDITIONS** → PO technical feasibility **ACCEPTED** (D-029) |
| Engineering status | `ACCEPTED` for technical feasibility only |
| Self-accept | **No** (PO acceptance recorded) |
| Date | 2026-11-26 |
| M03 checkpoint | `a99ad5ef7aced1e4c4fa970d314fa3048dc84885` |
| M04 commit | **AUTHORIZED** after validation; push **NO-GO** |
| Push / M05 commit / paid | Push **NO-GO**; M05 commit **NOT AUTHORIZED**; paid **NO-GO** |
| M05 / Ollama | M05 **GO** after M04 checkpoint; Ollama synthetic inference **AUTHORIZED** |

## 1. Executive summary

Focused remediation for F-M04-001..008. The fitness engine was **not** rebuilt. Gaps were primarily **evidence** and two real validator hardenings: (1) independent duration recalculation (do not trust declared `estimated_duration_minutes`), (2) template/experience/difficulty checks on externally constructed drafts. A reproducible evaluation CLI and expanded negative tests were added. Local quality gate **exit 0**. F-TRK-001..005 preserved.

## 2. Finding-by-finding remediation

### F-M04-001 — Independent Validator Evidence (HIGH)

| Field | Detail |
| --- | --- |
| Original concern | Validator independence from generator not sufficiently evidenced |
| Root cause / gap | Existing tests covered a subset; duration trusted declared field; template/difficulty not fully enforced on external drafts |
| Remediation | Expanded `validate_draft`; added `draft_parse.py` schema boundary; comprehensive constructed-draft negatives in `test_validator.py` |
| Evidence | `tests/fitness_engine/test_validator.py` (unknown/inactive/equipment/excluded/restriction/rule&catalog version/template/sets/reps/intensity/rest/schedule/duplicates/difficulty/duration/schema parse + schema-OK but domain-invalid LLM-shaped JSON) |
| Status | Remediated — awaiting TL accept |
| Limitations | In-process typed drafts remain the primary trust boundary; JSON parse is minimal for future LLM proposals |

### F-M04-002 — Safety Fail-Closed Evidence (HIGH)

| Field | Detail |
| --- | --- |
| Original concern | Unknown/missing safety info must not be treated as safe; preferences must not relax hard safety |
| Root cause / gap | Behavior largely present; evidence incomplete |
| Remediation | Added `test_safety_fail_closed.py` covering missing adult/config, symptoms vs preferences, non-adult, restriction walls, substitution cannot bypass tags, validator enforces restrictions on bypass drafts |
| Evidence | `tests/fitness_engine/test_safety.py`, `test_safety_fail_closed.py` |
| Status | Remediated — awaiting TL accept |
| Limitations | Not medical triage; keyword-agnostic concern block; no clinical claims |

### F-M04-003 — Schedule Hard vs Soft (MEDIUM)

| Field | Detail |
| --- | --- |
| Original concern | Ambiguity between hard schedule constraints and soft spacing |
| Root cause / gap | Documentation gap; consecutive-day soft behavior under-tested |
| Remediation | Documented in `docs/architecture/SCHEDULE_CONSTRAINTS_M04.md`; tests in `test_schedule_constraints.py` |
| Evidence | Hard: availability, uniqueness, template min_days. Soft: BR-SCHED-005 spacing preference; consecutive days allowed when forced |
| Status | Remediated — awaiting TL accept |
| Limitations | No hard consecutive-day ban; no week-boundary physiology model; no timezones |

### F-M04-004 — Duration Validation (MEDIUM)

| Field | Detail |
| --- | --- |
| Original concern | Validator trusted declared duration without recalculation |
| Root cause / gap | **Implementation defect** — declared minutes compared to max without recomputing from prescription |
| Remediation | Validator recalculates via `estimate_minutes`; emits `DECLARED_DURATION_MISMATCH` / `SESSION_DURATION_VIOLATION` |
| Evidence | `validator.py`, `test_duration_validation.py`, `test_validator.py` |
| Assumptions | warmup 180s + cooldown 120s + Σ(exec×sets) + rest×(sets-1) + transition 30s between exercises; round **up** to minutes; estimate ≠ actual workout |
| Status | Remediated — awaiting TL accept |
| Limitations | Tolerance currently 0 minutes |

### F-M04-005 — Reproducible Evaluation Runner (MEDIUM)

| Field | Detail |
| --- | --- |
| Original concern | Need stable local command + machine-readable report; no fragile latency gate |
| Root cause / gap | Dataset existed; dedicated CLI/report artifact missing |
| Remediation | `scripts/run_m04_evaluation.py` reuses `evaluation.py` scenarios (expected outcomes authored independently) |
| Evidence | Command below; artifact `docs/phase-00/m04-evaluation-report.json` |
| Status | Remediated — awaiting TL accept |
| Limitations | Latency reported for observability only |

**Reproduction command (repo root):**

```text
services\backend\.venv\Scripts\python.exe scripts\run_m04_evaluation.py --json docs\phase-00\m04-evaluation-report.json
```

Latest run: exit **0**; 32/32 scenarios; determinism_pass true; unknown IDs 0; invalid accepted 0; safety misses 0.

### F-M04-006 — Rule Traceability Coverage (LOW)

| Field | Detail |
| --- | --- |
| Original concern | Textual test refs ≠ executable coverage proof |
| Root cause / gap | Some `test_ref` paths pointed at non-existent filenames |
| Remediation | Fixed refs in `rules.py`; added `traceability.py` + `test_traceability.py` |
| Metrics (executed) | total 25; implemented 25; impl refs 25; test refs 25; verified executable 25; hard 24; hard w/ negative tests 24; provisional 4; expert-review-required 7; expert-approved **0**; deferred 0; unresolved refs none |
| Status | Remediated — awaiting TL accept |
| Limitations | Negative coverage map is maintained evidence, not full mutation testing |

### F-M04-007 — Completion Evidence (LOW)

| Field | Detail |
| --- | --- |
| Original concern | Completion report needed concrete samples + commands |
| Remediation | Samples below + this report; completion report cross-linked |
| Status | Remediated — awaiting TL accept |

#### Synthetic assessment (executed)

```text
goal=general_fitness
experience=beginner
equipment=[bodyweight]
days=[mon, wed, fri]
preferred=[mon, wed]
max_session_duration_minutes=45
adult_eligible=true
```

#### Generated draft (actual)

```text
outcome=VALIDATED_TECHNICAL_DRAFT
template=tmpl_home_bodyweight
days=[mon, wed]
session exercises (each day, 16 estimated minutes):
  ex_bw_squat x2, ex_pushup x2, ex_bw_good_morning x2, ex_dead_bug x2
```

#### Independent validation of that draft

```text
is_technically_validated=True; issues=[]
```

#### Directly constructed invalid draft

```text
exercise_id=ex_unknown_llm → UNKNOWN_EXERCISE_ID (BR-VAL-001); not technically validated
```

#### D-022..D-028 summary

| ID | Summary |
| --- | --- |
| D-022 | Versioned dataclass rule catalog `m04-provisional-1` |
| D-023 | Synthetic fixture catalog `fixture-v1` (no external ingest) |
| D-024 | Tie-break ascending `exercise_id` |
| D-025 | Structured `GenerationResult` / `ValidationIssue` |
| D-026 | Duration estimate assumptions |
| D-027 | Any reported concern → REVIEW_REQUIRED |
| D-028 | Evaluation scenarios + pytest/CLI gate |

#### Content licensing

- In use: **original synthetic fixtures only**.
- External datasets: **UNVERIFIED**, not ingested.
- App LICENSE: still PENDING (OI-014 / TB-011).
- Production exercise content: OI-005 remains **OPEN**.

#### Secret heuristic

Content-level scan for credential-like patterns on M04 modules/docs: hits only on the word “secret” in historical secret-scanning *documentation* (false positive). No API keys/tokens found in M04 engine sources. Heuristic limitation: keyword-based, not a full secret scanner.

#### Documentation links

Relative links in M04 architecture/business-rules/completion docs checked; no broken local targets found among scanned files.

### F-M04-008 — Incidental Foundation Changes (LOW)

| Field | Detail |
| --- | --- |
| Original concern | Working tree may mix M04 work with incidental format churn |
| Evidence | `git diff -w --numstat` vs `a99ad5e` for foundation `services/backend/app` and `apps/mobile` showed **no non-whitespace changes** |
| Classification | M04 domain/tests/docs = intentional; backend/Flutter tracked file mods = **formatting-only** (ruff/dart format for quality gate); `scripts/runtime-evidence/**` = local runtime artifacts — **exclude from future commit** |
| Status | Reviewed — awaiting TL accept |
| Limitations | Untracked evidence logs/pngs must stay out of commit scope |

## 3. Actual implementation defects discovered

1. **Duration trust defect (F-M04-004):** validator compared declared duration to max without recalculating — **fixed**.
2. **Incomplete external-draft enforcement:** template compatibility and experience/difficulty not fully applied on non-generator drafts — **hardened**.
3. **Stale rule `test_ref` paths** for duration/volume/intensity — **fixed**.

## 4. Findings resolved primarily through existing evidence

- Much of F-M04-002 safety fail-closed behavior already existed in `safety.py` / generator short-circuit.
- Schedule hard template min_days already failed closed; soft spacing already intentional.
- Evaluation dataset already authored expected outcomes independently of a single run.

## 5–6. Code / test changes (summary)

| Area | Change |
| --- | --- |
| `validator.py` | Recalc duration; template/experience/difficulty checks |
| `draft_parse.py` | Dict→draft schema boundary |
| `selector.py` | Public `difficulty_allowed` |
| `rules.py` | Correct test_ref paths |
| `traceability.py` | Metrics |
| `scripts/run_m04_evaluation.py` | CLI + JSON |
| Tests | Expanded validator/safety/schedule/duration/traceability |
| Docs | SCHEDULE_CONSTRAINTS_M04; this remediation report; eval JSON artifact |

## 7. Reproducible evaluation results

| Metric | Value |
| --- | --- |
| catalog_version | fixture-v1 |
| rule_set_version | m04-provisional-1 |
| scenarios | 32 (10/10 pos, 15/15 neg, 7/7 boundary) |
| failed IDs | [] |
| unknown exercise IDs | 0 |
| invalid drafts accepted | 0 |
| safety blocks missed | 0 |
| determinism | pass |
| latency | observability only (median ~0.08 ms this run) |

## 8. Final validation (executed this remediation)

| Check | Exit | Notes |
| --- | --- | --- |
| `ruff check app tests` | 0 | |
| `ruff format --check app tests` | 0 | |
| `pytest -q` | 0 | **88 passed** |
| `scripts/local_quality.ps1` | 0 | Backend + Flutter + compose |
| `scripts/run_m04_evaluation.py` | 0 | functional_pass true |
| Hosted GitHub Actions | — | **NOT_EXECUTED** (OI-015) |
| Ollama inference | — | **Not executed** |

## 9. Remaining blockers

- Tech Lead final acceptance of M04 (do not self-accept).
- OI-003 expert rule review; OI-005 production content licensing; OI-013..017 M03 follow-ups.
- M04 commit still **NOT AUTHORIZED**.

## 10. Final Git status

- Branch `main`; HEAD still M03 `a99ad5e…`
- Uncommitted M04 domain/tests/docs + incidental format-only foundation files
- Exclude `scripts/runtime-evidence/` from future staging
- **No commit / no push performed**

## 11. Updated acceptance checklist

| Item | Status |
| --- | --- |
| Independent validator negatives | Evidence added |
| Safety fail-closed | Evidence added |
| Schedule hard/soft documented | Done |
| Duration independently verified | Fixed + tested |
| Reproducible evaluation runner | Done |
| Rule traceability metrics | Done |
| Completion evidence samples | Done |
| Foundation diff review | Formatting-only confirmed |
| Self-accept / commit / push / M05 | **No** |

## 12. M05 readiness recommendation

**NO-GO** until Tech Lead final-accepts M04 and explicitly authorizes M05. Deterministic engine remains the hard-constraint boundary for any future LLM proposals.

**STOP** — awaiting final independent Tech Lead review.
