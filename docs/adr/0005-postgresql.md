# ADR-0005 — PostgreSQL as System of Record

| Field | Value |
| --- | --- |
| Status | `ACCEPTED` |
| Date | 2026-11-25 |

## Decision

PostgreSQL is the authoritative server datastore (SQLAlchemy + Alembic). Mobile SQLite is local durability for workouts, not global SoT.

## Alternatives

NoSQL-first — rejected for relational invariants (plans/versions/sets).

## Validation

M03 migrations; backup/PITR before beta.

## Approval (2026-11-25)

ACCEPTED by Tech Lead with Project Owner confirmation for PH00-M03 foundation bootstrap.
