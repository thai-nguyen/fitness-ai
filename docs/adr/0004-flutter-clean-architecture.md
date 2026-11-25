# ADR-0004 — Flutter Pragmatic Clean Architecture + BLoC

| Field | Value |
| --- | --- |
| Status | `ACCEPTED` |
| Date | 2026-11-25 |

## Decision

Flutter app uses pragmatic Clean Architecture with BLoC/Cubit, GoRouter, GetIt, Dio, Drift.

## Alternatives

Riverpod-only / MVC — rejected vs approved stack.

## Consequences

Feature folders with presentation/application/domain/data. Testability for offline sync.

## Validation

M03 walking skeleton + M06 offline POC.

## Approval (2026-11-25)

ACCEPTED by Tech Lead with Project Owner confirmation for PH00-M03 foundation bootstrap.
