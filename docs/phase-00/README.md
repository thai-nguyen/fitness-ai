# PHASE-00 — Project Initialization & Technical Discovery

## Objective

Reduce technical and product risk before production feature development through assessment, architecture, reversible foundations, and evidence-based POCs.

## Authorization

- GO: discovery, architecture documentation, technical POCs, reversible engineering foundation
- NO-GO: full production feature development, unapproved infrastructure commitments

## Milestones

| ID | Title | Status |
| --- | --- | --- |
| PH00-M01 | Repository Assessment & Project Baseline | **`ACCEPTED`** (Tech Lead 2026-11-25) |
| PH00-M02 | Architecture & Domain Modelling | **`ACCEPTED`** (Tech Lead 2026-11-25) |
| PH00-M03 | Engineering Foundation | `IN_PROGRESS` (GO after M02 checkpoint) |
| PH00-M04 | Fitness Engine & Content Feasibility | `NOT_STARTED` |
| PH00-M05 | AI Technical POCs | `NOT_STARTED` |
| PH00-M06 | Offline Workout POC | `NOT_STARTED` |
| PH00-M07 | Background Job Reliability POC | `NOT_STARTED` |
| PH00-M08 | Security, Privacy & Evaluation | `NOT_STARTED` |
| PH00-M09 | Phase 0 Exit Review | `NOT_STARTED` |

Live detail: [`execution-tracker.md`](execution-tracker.md).

## Protocol (every milestone)

1. Read relevant project documentation and repository instructions
2. Inspect current repository state
3. Identify dependencies and prerequisites
4. Produce an implementation plan
5. Identify assumptions and unresolved decisions
6. Implement only authorized scope
7. Run relevant validation and tests
8. Review for architecture, security, and quality
9. Update documentation and execution tracker
10. Produce milestone completion report
11. **Stop and wait for Tech Lead approval** before the next milestone

## Evidence rules

- Do not silently skip failed tests or acceptance criteria
- Do not fabricate benchmarks, test results, approvals, or completed deliverables
- Use explicit statuses from [`../README.md`](../README.md)
