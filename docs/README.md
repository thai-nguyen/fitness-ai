# Documentation Index

Source of truth for Phase 0 discovery, architecture decisions, risks, and execution tracking.

## Structure

```text
docs/
├── README.md                 # This index
├── baseline/                 # Project baseline and approved direction
├── phase-00/                 # Phase 0 milestones, tracker, evidence
├── architecture/             # System architecture (PH00-M02+)
├── business-rules/           # Fitness rule catalogs (PH00-M04+)
├── adr/                      # Architecture Decision Records
├── change-requests/          # Formal change control
├── risks/                    # Risk register
└── backlog/                  # Technical backlog derived from discovery
```

## How to use

1. Read root [`../AGENTS.md`](../AGENTS.md) for engineering/agent governance.
2. Read [`baseline/INDEX.md`](baseline/INDEX.md) for source-of-truth hierarchy and authoritative deposit status.
3. Read [`baseline/PROJECT_BASELINE.md`](baseline/PROJECT_BASELINE.md) for project state and constraints.
4. Track Phase 0 work in [`phase-00/execution-tracker.md`](phase-00/execution-tracker.md).
5. Record architecture decisions as ADRs under [`adr/`](adr/) (ADR-0001 exists; further ADRs in M02+).
6. Raise material deviations via [`change-requests/`](change-requests/).
7. Keep risks current in [`risks/RISK_REGISTER.md`](risks/RISK_REGISTER.md).
8. Phase 0 backlog: [`backlog/TECHNICAL_BACKLOG.md`](backlog/TECHNICAL_BACKLOG.md).

## Status vocabulary

| Status | Meaning |
| --- | --- |
| `NOT_STARTED` | Work has not begun |
| `IN_PROGRESS` | Actively being executed |
| `BLOCKED` | Cannot proceed without external input or approval |
| `IMPLEMENTED` | Work delivered; validation incomplete or pending |
| `VALIDATED` | Tests/evidence confirm acceptance criteria |
| `ACCEPTED` | Reviewer approved |
| `DEFERRED` | Intentionally postponed with rationale |

A task may only be marked `ACCEPTED` after the appropriate reviewer has approved it.

## Phase 0 status (summary)

| Milestone | Status |
| --- | --- |
| PH00-M01 | **`ACCEPTED`**; commit `dc5f9d2` |
| PH00-M02 | **`ACCEPTED`**; commit `6ecbbaf` |
| PH00-M03 | **`ACCEPTED` WITH WAIVER** (D-020); commit `a99ad5e` |
| PH00-M04 | **`ACCEPTED`**; commit `a7a870a` |
| PH00-M05 | `VALIDATED` engineering; TL acceptance PENDING; commit NOT AUTHORIZED |

Live detail: [`phase-00/execution-tracker.md`](phase-00/execution-tracker.md).

## Document ownership

| Document class | Owner | Approver |
| --- | --- | --- |
| Product scope / MVP | Product Owner | Product Owner + Tech Lead |
| Technical direction / ADRs | Tech Lead | Tech Lead |
| Phase 0 execution artifacts | Engineering | Tech Lead |
| Fitness business rules | Domain Expert | Domain Expert + Tech Lead |
| Change Requests | Requestor | Tech Lead (+ PO when product-impacting) |
