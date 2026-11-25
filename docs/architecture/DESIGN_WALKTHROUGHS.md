# Design Walkthroughs — Core MVP Scenarios

| Field | Value |
| --- | --- |
| Status | `IMPLEMENTED` (design analysis) |
| Milestone | PH00-M02 |
| Note | Not executed application tests |

| # | Scenario | Modules | Key transitions | Security | Failure / open |
| --- | --- | --- | --- | --- | --- |
| 1 | Onboarding → generate plan | Identity, Profile, Exercise, FitnessEngine, Coaching/Training | Draft→Validated | Owner authZ | Provider fail → fallback template |
| 2 | Accept validated plan | Training | Validated→Active; prior supersede atomic | Confirm | Conflict 409 |
| 3 | Offline workout complete | Workout, SQLite | InProgress→Completed; PendingSync | Local account scope | M06 POC |
| 4 | Restart mid offline workout | Workout | Resume InProgress | — | Local durability |
| 5 | Duplicate sync | Workout API | Idempotent event_id | Auth | Ack without dup |
| 6 | Exercise substitution | Training, FitnessEngine, Catalog | New Draft version or proposal | Confirm if material | Only eligible subs |
| 7 | Abnormal pain reported | Coaching, Safety | Safety card; no push intensify | AIR-006 | Expert copy pending |
| 8 | AI adjustment proposed | Coaching, FitnessEngine | Recommendation Validated | Tool authZ | Stale version guard |
| 9 | User rejects adjustment | Coaching | Rejected; no Training mutate | — | — |
| 10 | Accept stale adjustment | Coaching, Training | Expire/reject apply | Version check | Must not overwrite |
| 11 | AI provider unavailable | Coaching, Workout | Degraded chat; workouts OK | — | Quota UX |
| 12 | Update goals | Profile | profile.updated; invalidate proposals | Owner | Proposal expiry policy open |
| 13 | Delete memory | Coaching | Memory deleted; history kept | Owner | Distinct from account delete |
| 14 | Account deletion | Identity → all | Cascaded delete jobs | Strong auth | Backup retention pending M08 |

## Gaps (honest)

- Exact multi-device conflict algorithm open (M06)
- Expert safety copy/thresholds open (M04)
- Provider SLOs unmeasured
- Deletion backup retention policy open (M08)
