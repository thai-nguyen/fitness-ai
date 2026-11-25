# ADR-0001 — GitHub Hosting and GitHub Actions CI

| Field | Value |
| --- | --- |
| ADR ID | ADR-0001 |
| Title | Retain GitHub repository hosting; use GitHub Actions and Pull Request workflow |
| Status | `ACCEPTED` |
| Date proposed | 2026-11-25 |
| Date accepted | 2026-11-25 |
| Milestone | PH00-M01 final remediation (decision only; CI implementation deferred to PH00-M03) |
| Decision register | D-001 |
| Related finding | F-M01-002 |
| Approvers | Product Owner (explicit approval); Tech Lead |

## Context

- The repository remote is `https://github.com/thai-nguyen/fitness-ai.git`.
- The prior technical baseline / derived approved direction specified **GitLab CI**.
- No CI workflow files exist yet.
- Tech Lead proposed aligning CI/CD with the actual host rather than migrating hosting for Phase 0.
- Product Owner explicitly approved GitHub hosting, GitHub Actions, and Pull Request–based development.

## Decision (`ACCEPTED`)

1. **Retain GitHub** as the repository host.
2. Use **GitHub Actions** instead of GitLab CI.
3. Use a **Pull Request–based** development workflow.
4. Introduce **branch protection** and **required CI checks** during the appropriate milestone (**PH00-M03** for CI foundation; protection rules when the walking skeleton exists).
5. **Do not** create CI workflow files under this ADR until PH00-M03 is authorized.

**Supersession:** This accepted decision supersedes the original GitLab CI proposal in prior baseline wording. Historical documents that mentioned GitLab CI are retained for audit; derived working docs must reflect GitHub Actions going forward.

## Rationale

- Avoids a mid–Phase-0 hosting migration while the repo is documentation-only.
- Keeps CI colocated with the existing remote and GitHub PR model.
- Defers implementation cost to M03, when a walking skeleton can exercise real checks.
- Matches Product Owner explicit approval and Tech Lead recommendation.

## Alternatives considered

| Alternative | Pros | Cons | Why not chosen |
| --- | --- | --- | --- |
| A. Migrate remote to GitLab; keep GitLab CI | Matches prior TIP CI wording | Migration overhead; disrupts current remote | Higher cost for Phase 0; superseded by PO approval |
| B. Keep GitHub host + GitLab CI via mirroring | Preserves GitLab CI wording | Dual-tooling complexity | Premature operational complexity |
| C. Keep GitHub host + GitHub Actions (this ADR) | Matches current remote; simple PR workflow | Requires updating derived technical direction / TIP reconciliation | **Accepted** |
| D. Defer any CI decision to M09 | Avoids early ADR | Blocks M03 planning clarity | Decision confirmed |

## Consequences

### Positive

- Clear hosting/CI target for M03 planning.
- PR workflow is standard for the current remote.
- OI-002 can be closed after documentation synchronization.

### Negative / follow-ups

- Reconcile AUTH-003 (TIP v1.1) when deposited if it still names GitLab CI.
- External Cursor **GitLab workflow** plugin rule may still conflict with GitHub PR language (OI-006). Handled under D-005 constraints — do **not** modify global Cursor rules.
- CI workflows remain unimplemented until PH00-M03.

### Out of scope for this ADR

- Creating `.github/workflows/*`
- Enabling branch protection (M03+)
- Choosing exact CI jobs, runners, or coverage gates (M03)

## Approval

| Role | Decision | Date |
| --- | --- | --- |
| Product Owner | **Approved** (GitHub hosting, GitHub Actions, PR workflow) | 2026-11-25 |
| Tech Lead | **Accepted** | 2026-11-25 |

**Status: `ACCEPTED`.**
