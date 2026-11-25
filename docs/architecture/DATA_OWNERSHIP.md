# Data Ownership & Consistency Matrix

| Field | Value |
| --- | --- |
| Owner | Engineering (Architect) |
| Version | 0.1 |
| Status | `PROPOSED` (PH00-M02) |
| Related | AUTH-003 §3,5,6; privacy gates |

## Legend

| Sensitivity | Meaning |
| --- | --- |
| PII | Identity |
| Health-adj | Fitness/body/performance |
| Content | Catalog |
| Ops | Audit/usage |

| Consistency | Meaning |
| --- | --- |
| Strong | Single writer aggregate txn |
| Eventual | Projection / sync |
| Local-first | Mobile durable then sync |

## Matrix

| Data | Owner module | SoT | Writers | Readers | Mobile | Sync | Consistency | Sensitivity | Deletion |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| User identity | Identity | PG | Identity | All (id) | Token/profile cache | Login | Strong | PII | Cascade command |
| Consents | Identity | PG | Identity | Identity/Admin | Cache | Pull | Strong | PII | Soft+hard policy |
| Profile/goals/prefs/limitations | Profile | PG | Profile | Coaching/Training via API | Cache | Pull/push profile | Strong | Health-adj | With account |
| Assessments | Profile | PG | Profile | Training | Optional cache | Pull | Strong | Health-adj | With account |
| Exercises | Exercise | PG | Admin | All authenticated | Catalog cache | Pull approved | Strong | Content | Retire not hard-delete if referenced |
| Training plans/versions | Training | PG | Training | Workout/Coaching | Active plan cache | Pull; activate online preferred | Strong | Low-Med | Soft archive |
| Adjustment proposals | Training/Coaching | PG | Coaching proposes; Training applies | User | Cards cache | Online | Strong | Low | Expire |
| Workout sessions/sets | Workout | PG (+ local SQLite) | Workout (+ mobile offline) | Progress/Coaching | **Local SoT until synced** | Event batch | Local-first → Strong | Health-adj | With account |
| Workout feedback | Workout | PG | Workout | Coaching | Local then sync | Event | Strong | Health-adj | With account |
| Recovery check-ins | Recovery | PG | Recovery | Coaching | Optional | Push | Strong | Health-adj | With account |
| Body measurements | Progress | PG | Progress | Progress/Coaching | Local entry | Push | Strong | Health-adj | With account |
| Progress snapshots | Progress | PG projection | Progress projector | User | Cache | Pull | Eventual | Health-adj | Rebuild/delete |
| Conversations/messages | Coaching | PG | Coaching | User | Cache recent | Pull/SSE | Strong | PII/health-adj | User/account delete |
| Memory items | Coaching | PG | Coaching (user edit/delete) | Coaching tools | List UI | Pull | Strong | Health-adj | User delete ≠ history delete |
| Recommendations | Coaching | PG | Coaching | User/Training | Cards | Pull | Strong | Low | Expire |
| Notification prefs | Notification | PG | Notification | Worker | Prefs cache | Push | Strong | PII | With account |
| Analytics events | Platform | Analytics vendor | API | Ops | — | Fire-and-forget | Best-effort | **No raw health/chat/PII** | Vendor policy TBD |
| Audit | Platform | PG | Platform | Admin | — | — | Append-only | Ops/PII refs | Retention policy |
| AI usage | Platform | PG | Coaching/Worker | Admin | — | — | Append-only | Ops | Retention |
| Jobs/outbox | Platform | PG | Producers/Worker | Worker | — | — | Strong claim | Ops | TTL |

## Rules

1. **AI memory never overrides** Profile/Training/Workout SoT.
2. **No cross-module repository writes.**
3. **Optimistic concurrency** on TrainingPlan header and Recommendation apply.
4. **Idempotency** on workout sync `event_id` + recommendation apply.
5. **Derived progress** regenerated from workouts; not authoritative.
6. **Limited outbox:** plan_activated/updated → reminders; workout.completed → progress; user.deletion_requested → cascade.
7. Jurisdiction/legal basis/provider retention — **PENDING** (OI-012).

## Validation

Threat model M08; offline POC M06; deletion E2E before beta.
