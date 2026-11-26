# M05 Prompt Inventory

| Prompt ID | Version | Purpose | Input | Output | Limitations |
| --- | --- | --- | --- | --- | --- |
| SYS-COACH-001 | 1 | System coaching instructions (synthetic) | n/a | text | Not medical advice |
| GEN-PERSONALIZE-001 | 1 | Bounded training personalization | candidates + assessment | JSON proposal | Eligible IDs only |
| GEN-REPAIR-001 | 1 | One-shot structured repair | prior JSON + errors | JSON proposal | Max 1 attempt |
| EXPLAIN-PLAN-001 | 1 | Explain technical draft | draft summary | text | No new prescriptions |
| MEM-EXTRACT-001 | 1 | Extract supported preference candidate | utterance | JSON candidate | Allowlisted types |
| SAFETY-DECLINE-001 | 1 | Unsupported/unsafe decline phrasing | reason code | text | Deterministic gates still apply |

All prompts treat user text and memory as **data**, not instructions.
