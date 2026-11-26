"""Technical safety screening (not medical clearance)."""

from __future__ import annotations

from app.modules.fitness_engine.domain.assessment import AssessmentInput
from app.modules.fitness_engine.domain.enums import SafetyOutcome, Severity
from app.modules.fitness_engine.domain.results import SafetyScreenResult, ValidationIssue
from app.modules.fitness_engine.domain.rules import RULE_SET_VERSION


def screen_safety(
    assessment: AssessmentInput,
    *,
    rule_set_version: str | None = RULE_SET_VERSION,
) -> SafetyScreenResult:
    issues: list[ValidationIssue] = []

    if not rule_set_version:
        return SafetyScreenResult(
            outcome=SafetyOutcome.REJECTED,
            issues=(
                ValidationIssue(
                    code="MISSING_SAFETY_CONFIGURATION",
                    rule_id="BR-SAFE-003",
                    field="rule_set_version",
                    severity=Severity.ERROR,
                    reason="safety rule configuration missing; fail closed",
                ),
            ),
            guidance_category=None,
        )

    if assessment.adult_eligible is None:
        return SafetyScreenResult(
            outcome=SafetyOutcome.INSUFFICIENT_INFORMATION,
            issues=(
                ValidationIssue(
                    code="MISSING_ADULT_ELIGIBILITY",
                    rule_id="BR-SAFE-001",
                    field="adult_eligible",
                    severity=Severity.ERROR,
                    reason="adult eligibility not provided",
                ),
            ),
            guidance_category=None,
        )

    if assessment.adult_eligible is False:
        return SafetyScreenResult(
            outcome=SafetyOutcome.REJECTED,
            issues=(
                ValidationIssue(
                    code="UNSUPPORTED_AGE_ELIGIBILITY",
                    rule_id="BR-SCOPE-002",
                    field="adult_eligible",
                    severity=Severity.ERROR,
                    reason="non-adult profiles are unsupported",
                ),
            ),
            guidance_category="unsupported_population",
        )

    if assessment.reported_pain_or_safety_concerns:
        return SafetyScreenResult(
            outcome=SafetyOutcome.REVIEW_REQUIRED,
            issues=(
                ValidationIssue(
                    code="REPORTED_SAFETY_CONCERN",
                    rule_id="BR-SAFE-002",
                    field="reported_pain_or_safety_concerns",
                    severity=Severity.ERROR,
                    reason=(
                        "automated plan generation blocked due to reported concerns; "
                        "seek qualified professional review (not a diagnosis)"
                    ),
                ),
            ),
            guidance_category="professional_review_or_urgent_care_guidance",
        )

    if not assessment.assessment_complete:
        return SafetyScreenResult(
            outcome=SafetyOutcome.INSUFFICIENT_INFORMATION,
            issues=(
                ValidationIssue(
                    code="INCOMPLETE_ASSESSMENT",
                    rule_id="BR-ASSESS-003",
                    field="assessment_complete",
                    severity=Severity.ERROR,
                    reason="critical assessment information incomplete",
                ),
            ),
            guidance_category=None,
        )

    return SafetyScreenResult(
        outcome=SafetyOutcome.PASSED_TECHNICAL_CHECKS,
        issues=tuple(issues),
        guidance_category=None,
    )
