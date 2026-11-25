# Product → Architecture Traceability (Seed)

| Field | Value |
| --- | --- |
| Status | `IMPLEMENTED` (seed; full story-level mapping deferred to **M09**) |
| Version | 0.2 (F-M02-002 remediation) |
| Rule | Preserve Product Plan feature family IDs; **do not invent** missing story IDs |

## Glossary (naming disambiguation)

| Term | Meaning |
| --- | --- |
| **Baseline AUTH-001..004** | Authoritative *documents* under `docs/baseline/authoritative/` (Product Plan, PO Review, TIP, Baseline Index) |
| **Feature family `AUTH-001–006`** | *Authentication* product capabilities in Product Plan v1.0 backlog inventory |
| **PH00-TB-*** | Phase 0 *technical* backlog tasks |

These namespaces collide on the string `AUTH-` but refer to **different** things. This matrix uses **feature family** IDs from the Product Plan unless marked “baseline doc”.

## Core MVP P0 coverage

| Feature family | Priority | Owning context | Architecture component(s) | Tech task (Phase 0) | Validation milestone | Coverage | Open dependency |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AUTH-001–006 (Authentication) | P0 | Identity | OIDC gateway, session/token, account deletion | PH00-TB-010 | M03 auth spike | **Covered** | Auth vendor TBD (prefer zero-cost) — ADR-0013 |
| ONB-001–009 (Onboarding) | P0 | Profile + Training + Coaching | Profile aggregates; plan generation flow | PH00-TB-010, 012, 014 | M03–M05; walkthroughs 1–2 | **Covered** | Expert thresholds M04 |
| EXL-001–004 (Exercise library) | P0 | Exercise Catalog | Exercise aggregate; admin review | PH00-TB-012, 013 | M04 | **Covered** | Content licensing |
| TRN-001–012 (Training plans) | P0 | Training + Fitness Engine | Plan/version/day/planned exercise; substitution | PH00-TB-010, 012, 014 | M03–M05; ADR-0010 | **Covered** | Exact transition polish M03 |
| WKT-001–011 (Workout + offline) | P0 | Workout | Session/set; offline sync | PH00-TB-010, 015 | M03, **M06** | **Covered** | Multi-device conflict OPEN |
| AI-001–013 (Coach) | P0 | Coaching | Orchestrator, memory, cards, Ollama adapter | PH00-TB-014 | **M05**, M08 | **Covered** | Qwen suitability PENDING |
| REC-001 (Post-workout feedback) | P0 | Workout + Coaching | WorkoutFeedback; adaptive proposal input | PH00-TB-014 | M05; walkthrough 7–8 | **Covered** | Expert safety copy |
| PRG-001–005 (Progress) | P0 | Progress | BodyMeasurement; ProgressSnapshot projection | PH00-TB-010+ | M03+ | **Covered** | Eventual consistency OK |
| NTF-001–003 (Reminders) | P0 | Notification | Prefs; jobs/outbox → push | PH00-TB-010, 016 | M03, M07 | **Covered** | Push free-tier limits; PG jobs POC |
| ADM-001–006 (Minimal admin) | P0 (subset) | Administration | Admin RBAC, catalog review, usage | Later slices post-M03 | Beta gate | **Partial** | Which ADM subset for alpha vs beta — clarify at G4/G6; no new IDs invented |
| OPS-001–003 (Errors/cost/audit) | P0 | Platform | Audit, AI usage, basic logging | PH00-TB-010, 017 | M03, M08 | **Covered** | — |
| Privacy/consent/AI safety (MVP_SCOPE) | P0 | Identity + Coaching + Platform | ConsentRecord; guardrails; ADR-0015/0016/0017 | PH00-TB-017, 014 | M05, M08 | **Covered** | Jurisdiction PENDING |
| Product analytics (privacy-safe) | P0 | Platform | Analytics adapter (OSS preferred) | PH00-TB-010+ | M03+ | **Partial** | Vendor/OSS choice PENDING; no raw health/chat |

## Non-P0 (explicitly out of Core MVP commitment)

| Feature family | Priority | Coverage note |
| --- | --- | --- |
| Nutrition Lite (NUT subset) | Conditional P1 | Architecture deferred; spike only |
| Progressive overload / PRs | P1 | ProgressionPolicy pending expert |
| Entitlement foundation | P1 | No production billing |
| NUT full / SUB / SOC / RUN / INT | Deferred | Not designed beyond exclusion |

## Ambiguities / gaps (honest)

1. **Naming collision** `AUTH-*` document vs feature family — clarified above.
2. **Minimal admin subset** for alpha vs beta not ID-split in Product Plan — marked Partial.
3. **Analytics** called out in MVP_SCOPE without a dedicated Product Plan family ID in the seed inventory — mapped under Platform without inventing IDs.
4. Full US-level traceability → **M09**.

## Linked Phase 0 design tasks

`PH00-TB-008`, `PH00-TB-009` (done as design). Implementation/validation: TB-010+.
