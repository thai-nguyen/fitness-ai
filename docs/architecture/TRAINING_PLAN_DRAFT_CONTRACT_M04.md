# Training Plan Draft Contract (PH00-M04)

| Field | Value |
| --- | --- |
| Schema version | `1.0.0` |
| Rule set version | `m04-provisional-1` |
| Lifecycle | **Technical draft only** — never activated in M04 |

## Structure

```text
TrainingPlanDraft
  schema_version
  rule_set_version
  catalog_version
  template_id
  goal
  experience_level
  training_days[]
  sessions[]
    day
    estimated_duration_minutes
    exercises[]
      exercise_id
      working_sets
      intensity { repetition_range, effort_guidance, rpe, rest_seconds, intensity_policy_version }
  warnings[]
  validation_status
  review_status
```

## Generation outcomes

`VALIDATED_TECHNICAL_DRAFT` · `INVALID_INPUT` · `UNSUPPORTED_PROFILE` · `REVIEW_REQUIRED` · `INSUFFICIENT_CATALOG` · `INFEASIBLE_CONSTRAINTS` · `VALIDATION_FAILED`

## AI boundary (M05 prep; not implemented)

LLM may interpret preferences / explain / propose candidates. Deterministic engine remains responsible for hard constraints, eligibility, schedule feasibility, safety, and final technical acceptance. No Ollama calls in M04.
