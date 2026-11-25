# ADR-0009 — Offline-First Workout Tracking

| Field | Value |
| --- | --- |
| Status | `ACCEPTED` (architectural direction); implementation details remain PENDING until POC/evidence |
| Date | 2026-11-25 |

## Decision

Workouts are offline-first with Drift/SQLite, pending event log, idempotent sync. Business state separated from sync state.

## Validation

PH00-M06 POC acceptance criteria in AUTH-003.

## Approval scope (2026-11-25)

**Accepted:** architectural principle / direction only (Tech Lead + Project Owner).
**Not accepted as proven:** feasibility, schemas, algorithms, or production readiness � remain PENDING for the validation milestones named in this ADR.
