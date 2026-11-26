# Safety Policy (PH00-M04) — Technical Screening Only

| Field | Value |
| --- | --- |
| Implementation | `fitness_engine/domain/safety.py` |
| Claim | **Not** medical clearance; **not** diagnosis |

## Outcomes

| Outcome | Meaning |
| --- | --- |
| `PASSED_TECHNICAL_CHECKS` | No blocking technical safety flags |
| `REJECTED` | Unsupported population / missing config |
| `REVIEW_REQUIRED` | Reported concerns — block auto-generation |
| `INSUFFICIENT_INFORMATION` | Critical fields missing (fail closed) |

## Rules

- BR-SAFE-001 adult eligibility required
- BR-SAFE-002 any reported pain/safety concern → `REVIEW_REQUIRED` + guidance category `professional_review_or_urgent_care_guidance`
- BR-SAFE-003 missing rule-set configuration → reject

Does **not** implement medical triage or recommend exercising through concerning symptoms.
