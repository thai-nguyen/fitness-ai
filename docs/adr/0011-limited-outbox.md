# ADR-0011 — Limited Transactional Outbox

| Field | Value |
| --- | --- |
| Status | `PROPOSED` |
| Date | 2026-11-25 |

## Decision

Use a **limited** transactional outbox for durable cross-cutting reactions (plan activated → reminders; workout completed → progress; deletion cascade). No Kafka/generic event platform.

## Alternatives

Always sync in-request — fragile across worker. Full event bus — deferred.

## Validation

M03 schema; M07 job reliability overlaps.
