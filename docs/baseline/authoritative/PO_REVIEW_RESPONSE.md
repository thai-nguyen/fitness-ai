# PO Review Response — Consolidated reconstruction

Status: PROPOSED replacement baseline; historical PO/TL alignment summarized, not verbatim. Project Owner ratification pending. Product decisions here supersede conflicting early product-plan proposals.

## Review verdict
Conditional approval of discovery, prototype, POCs and reversible foundation. No authorization for full MVP development or a committed 16-week delivery until Phase 0 exit. Preserve product value and validate early; do not turn Phase 0 into speculative infrastructure work.

## Disposition of original TL change requests
| CR | Disposition | Product constraint |
|---|---|---|
| CR-001 | Partial | Retain basic weight loss, muscle, strength and general fitness; defer endurance |
| CR-002 | Accepted alignment | AI POC early |
| CR-003 | Accepted alignment | Deterministic Fitness Engine, limited V1 |
| CR-004 | Accepted alignment | Offline workout P0 |
| CR-005 | Accepted alignment | Evaluation from Phase 0 |
| CR-006 | Accepted alignment | Immutable plan versions |
| CR-007 | Accepted alignment | Consent/privacy |
| CR-008 | Accepted alignment | Content feasibility and rights |
| CR-009 | Accepted alignment | Entitlement foundation P1, no production billing MVP |
| CR-010 | Accepted alignment | Basic adaptive coaching P0 |
| CR-011 | Partial | Only justified durable events/outbox; no generic event platform |

## PO change requests and TL v1.1 disposition
| ID | Requirement | Priority | Disposition |
|---|---|---|---|
| PO-CR-001 | Keep basic weight loss | P0 | Aligned |
| PO-CR-002 | Prototype first two weeks | P0 | Aligned, target |
| PO-CR-003 | Vertical slices | P0 | Aligned |
| PO-CR-004 | Alpha before week 9 | P0 | Conditional on safety/readiness |
| PO-CR-005 | Limited fitness engine | P0 | Aligned |
| PO-CR-006 | Product analytics | P0 | Aligned |
| PO-CR-007 | Product gates | P0 | Aligned |
| PO-CR-008 | Design gate | P0 | Aligned |
| PO-CR-009 | Nutrition Lite separate estimate | P1 | Conditional, spike only now |
| PO-CR-010 | Limited event infrastructure | P1 | Aligned |
| PO-CR-011 | Redis/Celery assessment | P1 | Aligned; not mandatory |
| PO-CR-012 | AI failure UX | P0 | Aligned |
| PO-CR-013 | Memory management | P0 | Aligned |
| PO-CR-014 | Role/workstream re-estimate | P0 | Aligned |
| PO-CR-015 | Traceability | P0 | Aligned |
| PO-CR-016 | Research and validation | P0 | Aligned |
| PO-CR-017 | Provider data governance | P0 | Aligned |
| PO-CR-018 | Commercial unit economics before phase 2 | P1 | Aligned |

## Product acceptance scenarios
- Onboarding unaided; plan respects goal, equipment, experience, available days, rest and approved limitations. Preview and confirm; no silent activation.
- Home user without gym equipment receives eligible exercises. Three-day availability yields compatible schedule. Abnormal pain triggers safety guidance, not encouragement to continue.
- Start, log, time, complete and resume workout offline after process death. Sync without duplicate committed sets or loss; history references original plan version.
- AI uses authoritative profile/history; preference updates are explicit and editable; hypothetical statements do not overwrite facts. Account isolation and memory deletion tested.
- Missed workout or fatigue yields appropriate proposal, explanation and accept/reject. No unsafe load increase. Stale proposal cannot overwrite new plan; rejection changes nothing.
- Provider outage/quota does not prevent existing workouts. Timeout/retry, invalid-plan fallback, missing context clarification and transparent quota states.
- Progress reflects committed data; reminders respect preferences; account deletion, consent and data access work; no critical usability/accessibility blockers.

## AI product rules
AIR-001 no diagnosis; AIR-002 no autonomous goal changes; AIR-003 no autonomous activation; AIR-004 approved exercise IDs; AIR-005 no extreme weight-loss advice; AIR-006 no pushing through abnormal pain; AIR-007 distinguish facts/inference; AIR-008 memory cannot override domain truth; AIR-009 reject recommendations; AIR-010 safe fallback; AIR-011 view/edit/delete memory; AIR-012 scoped tool permissions. Expert approval of numerical fitness/nutrition thresholds remains pending.

## Product validation and analytics
HYP-001 personalized plan vs self-designed; 002 AI vs static; 003 memory value; 004 feedback adaptation; 005 Nutrition Lite demand; 006 annual willingness to pay; 007 proactive adherence without annoyance. Proposed research samples and metrics in Product Plan. Track onboarding_started/step_completed/completed, training_plan_generated/accepted/rejected, workout_started/completed/abandoned, coach_message_sent/response_rated, adjustment_proposed/accepted/rejected, notification_opened. No raw health data, chat or PII in analytics. Deduplicate event IDs; server authoritative for committed actions.

## Design and release gates
Prototype before production feature build; design tokens, navigation, low-friction logging, accessibility, offline/loading/error/empty states and recommendation cards. Alpha target week 8: onboarding→plan→workout→feedback→basic coaching. External alpha requires applicable safety/privacy gates first; otherwise synthetic/internal only. Beta target week 16 subject to evidence and resources. No advanced memory/adaptation or full admin required for alpha; required MVP capabilities for beta. Nutrition Lite only after alpha value validation, expert rules, separate estimate and capacity approval.

## Governance
PO owns vision, scope, priority, UX and product acceptance; PO+expert business rules; TL architecture, implementation and estimate; TL+expert+PO safety; TL+QA readiness; sponsor/project owner resources/budget. No silent scope changes. Preserve product feature IDs; link EPIC/FEAT/US/TASK/TEST/EVAL/ADR/RISK/CR. Each change records rationale, product/effort/timeline impact, dependencies, risks, alternatives and approval. Phase 0 exit requires product research/prototype, technical evidence, content rights/rules, security/provider governance, traceable backlog, role estimate and joint Go/No-Go. No actual research, expert approval or budget is implied by this document.
