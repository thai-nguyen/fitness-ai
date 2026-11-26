# PH00-M04 Evaluation Scenarios

| Field | Value |
| --- | --- |
| Dataset | `app/modules/fitness_engine/domain/evaluation.py` |
| Runner | `tests/fitness_engine/test_evaluation.py` |
| Data | Synthetic only |

## Summary (executed locally)

| Metric | Result |
| --- | --- |
| Scenario count | 32 |
| Positive pass | 10/10 |
| Negative pass | 15/15 |
| Boundary pass | 7/7 |
| All pass | Yes |
| Unknown exercise IDs in validated drafts | 0 |
| Invalid drafts accepted as validated | 0 (within dataset) |

Scenario IDs: `S-POS-001`…`S-POS-010`, `S-NEG-001`…`S-NEG-015`, `S-BND-001`…`S-BND-007`.

Each scenario records ID, description, input, expected outcomes, rule refs, actual outcome, pass/fail via the evaluation runner.
