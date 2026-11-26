# Deterministic Fitness Engine Architecture

| Field | Value |
| --- | --- |
| Owner | Engineering + Domain Expert (rules) |
| Version | 0.2 |
| Status | `IMPLEMENTED` (PH00-M04 technical feasibility; expert approval PENDING) |
| Related | AUTH-003 §4, PO-CR-005, PH00-M04, PH00-TB-012 |
| Critical | **No invented expert approvals**; provisional thresholds are fixture-only |

## 1. Role

Pure deterministic domain service used by Training and Coaching. Not a separate deployable. Final authority on plan **validity** relative to encoded constraints; LLM cannot bypass it.

## 2. Components (conceptual)

| Component | Responsibility | Status |
| --- | --- | --- |
| ExerciseSelector | Filter eligible exercises by equipment/limitations/tags | `IMPLEMENTED` (M04 pure domain) |
| TrainingTemplate | Template-first skeletons by goal/availability | `IMPLEMENTED` (provisional templates) |
| SchedulePolicy | Map sessions to available days + rest | `IMPLEMENTED` |
| TrainingVolumeCalculator | Aggregate volume metrics for validation | `IMPLEMENTED` (provisional caps) |
| IntensityPolicy | Intensity bounds placeholders | `IMPLEMENTED` provisional; **expert review required** |
| SafetyPolicy | Hard stops (pain flags, contraindication tags) | `IMPLEMENTED` technical screening |
| SubstitutionPolicy | Same substitution group / constraints | `IMPLEMENTED` |
| ProgressionPolicy | Basic overload suggestions | **P1 + expert** (not M04) |
| RecoveryPolicy | Light recovery adjustments | Deferred beyond soft schedule spacing |
| TrainingPlanValidator | Compose all checks → pass/fail + reasons | `IMPLEMENTED` (independent of generator) |
| TrainingPlanGenerator | Deterministic pipeline → draft | `IMPLEMENTED` (no LLM) |

Code root: `services/backend/app/modules/fitness_engine/domain/` (+ `exercise_catalog`). See also [`EXERCISE_SCHEMA_AND_CATALOG_M04.md`](EXERCISE_SCHEMA_AND_CATALOG_M04.md), [`TRAINING_PLAN_DRAFT_CONTRACT_M04.md`](TRAINING_PLAN_DRAFT_CONTRACT_M04.md), [`SAFETY_POLICY_M04.md`](SAFETY_POLICY_M04.md), [`../business-rules/FITNESS_BUSINESS_RULES_M04.md`](../business-rules/FITNESS_BUSINESS_RULES_M04.md).

## 3. Constraint classes

| Class | Examples | Authority |
| --- | --- | --- |
| Hard | Only approved exercise IDs; respect explicit limitations tags; no activate without validation | Engineering + product |
| Configurable | Template choice, session count within availability | Product config |
| Expert-reviewed | Load progression %, forbidden intensifications | **Pending M04** |
| AI personalization | Wording, ordering within eligible set | LLM after deterministic filter |
| Research pending | Optimal periodization, fatigue models | Deferred |

## 4. Template-first generation

1. Inputs: profile, goals, experience, equipment, availability, limitations
2. Select approved template
3. Deterministic exercise eligibility
4. Optional LLM personalization **within** eligible set
5. Schema validate
6. FitnessEngine validate
7. Persist Draft → user confirm → Active

Bounded repair then vetted fallback or reject/clarify.

## 5. Contracts (conceptual)

**Input:** `FitnessContext` (structured profile slice), `PlanCandidate`
**Output:** `ValidationResult { ok, errors[], warnings[] }`
**Errors:** `UNAPPROVED_EXERCISE`, `CONSTRAINT_VIOLATION`, `SCHEDULE_INFEASIBLE`, `SAFETY_BLOCK`, `SCHEMA_INVALID`

## 6. Traceability

| Product need | Engine touchpoint |
| --- | --- |
| ONB-009 / AI-007 plan generation | Template + validator |
| TRN-008 substitution | SubstitutionPolicy |
| TRN-010 versioning | Validator on each version |
| AIR-004 approved IDs | Hard check |
| AIR-005/006 safety | SafetyPolicy |
| REC-001 feedback adaptation | Inputs to proposal validation |

## 7. Open dependencies (PH00-M04)

- Expert-approved numerical rules
- Content licensing for catalog
- Exact contraindication taxonomy
- ProgressionPolicy acceptance

**Do not invent prescriptions to unblock M02.**
