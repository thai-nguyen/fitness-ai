# Exercise Schema & Fixture Catalog (PH00-M04)

| Field | Value |
| --- | --- |
| Catalog version | `fixture-v1` |
| Implementation | `app/modules/exercise_catalog/domain/` |
| Status | Technical fixtures only |

## Schema

`ExerciseDefinition` fields: `exercise_id`, `name`, `description`, `primary_muscle_groups`, `secondary_muscle_groups`, `movement_pattern`, `equipment_requirements`, `difficulty`, `instruction_steps`, `contraindication_tags`, `substitution_group`, `estimated_duration_seconds`, `media_reference`, `content_source`, `license_status`, `review_status`, `active_status`.

Controlled enums: `MuscleGroup`, `MovementPattern`, `Equipment`, `Difficulty`, `ReviewStatus`, `LicenseStatus`.

Validation (`validate_catalog`): duplicate IDs, empty required fields, non-positive duration, missing substitution group.

## Fixture statistics

| Metric | Value |
| --- | --- |
| Exercise count | 26 |
| Active | 25 |
| Inactive (negative tests) | 1 |
| Environments covered | bodyweight, dumbbell, barbell/gym, machine/cable, band, kettlebell |
| Provenance | `original_synthetic_m04_fixture` |
| License status | `original_synthetic` |
| Review status | `technical_fixture` |

## Provenance & licensing evaluation

| Source | URL | License | Commercial use | Redistribution | Attribution | Modification | Media | Verified | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Original synthetic metadata (this repo) | n/a | Original / repo license PENDING (OI-014) | Subject to future LICENSE | Subject to future LICENSE | n/a | Yes (internal) | No media ingested | 2026-11-26 | Safe for M04 fixtures |
| Open exercise datasets (generic candidates) | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | Often separate | — | **Not ingested** |
| Commercial fitness apps | — | Proprietary | No | No | — | No | No | — | **Do not scrape** |
| Public-domain instructional text | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | — | — | — | — | Not used in M04 |

Repository application `LICENSE` remains PENDING PO (OI-014 / PH00-TB-011). Exercise content licensing for production remains OI-005.
