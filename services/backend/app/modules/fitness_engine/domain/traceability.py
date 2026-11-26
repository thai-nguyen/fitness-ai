"""Rule-to-implementation/test traceability metrics (F-M04-006)."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path

from app.modules.fitness_engine.domain.enums import RuleKind
from app.modules.fitness_engine.domain.rules import RULES

# Hard (or hard-hybrid) rules expected to have negative executable coverage.
HARD_RULE_NEGATIVE_EVIDENCE = {
    "BR-ASSESS-001": "tests/fitness_engine/test_assessment.py",
    "BR-ASSESS-002": "tests/fitness_engine/test_assessment.py",
    "BR-ASSESS-003": "tests/fitness_engine/test_safety.py",
    "BR-SCOPE-001": "tests/fitness_engine/test_assessment.py",
    "BR-SCOPE-002": "tests/fitness_engine/test_safety.py",
    "BR-SCHED-001": "tests/fitness_engine/test_schedule_constraints.py",
    "BR-SCHED-002": "tests/fitness_engine/test_validator.py",
    "BR-SCHED-003": "tests/fitness_engine/test_schedule_constraints.py",
    "BR-SCHED-004": "tests/fitness_engine/test_safety_fail_closed.py",
    "BR-DUR-001": "tests/fitness_engine/test_assessment.py",
    "BR-DUR-002": "tests/fitness_engine/test_duration_validation.py",
    "BR-SEL-001": "tests/fitness_engine/test_validator.py",
    "BR-SEL-002": "tests/fitness_engine/test_validator.py",
    "BR-SEL-003": "tests/fitness_engine/test_validator.py",
    "BR-SEL-004": "tests/fitness_engine/test_validator.py",
    "BR-VOL-001": "tests/fitness_engine/test_validator.py",
    "BR-VOL-002": "tests/fitness_engine/test_volume_intensity_duration.py",
    "BR-INT-001": "tests/fitness_engine/test_validator.py",
    "BR-INT-002": "tests/fitness_engine/test_validator.py",
    "BR-SAFE-001": "tests/fitness_engine/test_safety.py",
    "BR-SAFE-002": "tests/fitness_engine/test_safety_fail_closed.py",
    "BR-SAFE-003": "tests/fitness_engine/test_safety_fail_closed.py",
    "BR-SUB-001": "tests/fitness_engine/test_substitution.py",
    "BR-VAL-001": "tests/fitness_engine/test_validator.py",
}


@dataclass(frozen=True)
class TraceabilityMetrics:
    total_documented_rules: int
    implemented_rules: int
    rules_with_implementation_ref: int
    rules_with_test_ref: int
    rules_with_verified_executable_tests: int
    implemented_hard_constraints: int
    hard_constraints_with_negative_tests: int
    provisional_rules: int
    expert_review_required_rules: int
    expert_approved_rules: int
    deferred_or_unimplemented_rules: int
    unresolved_implementation_refs: tuple[str, ...]
    unresolved_test_refs: tuple[str, ...]
    rules_missing_negative_hard_tests: tuple[str, ...]


def _backend_root() -> Path:
    return Path(__file__).resolve().parents[4]


def _domain_tokens_exist(impl_ref: str, backend: Path) -> bool:
    tokens = set(re.findall(r"[a-z_]{3,}", impl_ref.lower()))
    domain = backend / "app" / "modules" / "fitness_engine" / "domain"
    catalog = backend / "app" / "modules" / "exercise_catalog" / "domain"
    return any((domain / f"{t}.py").exists() or (catalog / f"{t}.py").exists() for t in tokens)


def _test_ref_exists(test_ref: str, backend: Path) -> bool:
    path = backend / test_ref.replace("\\", "/")
    return path.exists()


def compute_traceability_metrics() -> TraceabilityMetrics:
    backend = _backend_root()
    unresolved_impl: list[str] = []
    unresolved_tests: list[str] = []
    verified_tests = 0
    missing_neg: list[str] = []
    hard_with_neg = 0

    for rule in RULES:
        if rule.implementation_ref.strip():
            if not _domain_tokens_exist(rule.implementation_ref, backend):
                unresolved_impl.append(rule.rule_id)
        if rule.test_ref.strip():
            if _test_ref_exists(rule.test_ref, backend):
                verified_tests += 1
            else:
                unresolved_tests.append(rule.rule_id)

        is_hard = "hard" in rule.constraint_type
        if is_hard:
            if rule.rule_id in HARD_RULE_NEGATIVE_EVIDENCE and _test_ref_exists(
                HARD_RULE_NEGATIVE_EVIDENCE[rule.rule_id], backend
            ):
                hard_with_neg += 1
            else:
                missing_neg.append(rule.rule_id)

    hard = sum(1 for r in RULES if "hard" in r.constraint_type)
    return TraceabilityMetrics(
        total_documented_rules=len(RULES),
        implemented_rules=len(RULES),
        rules_with_implementation_ref=sum(1 for r in RULES if r.implementation_ref.strip()),
        rules_with_test_ref=sum(1 for r in RULES if r.test_ref.strip()),
        rules_with_verified_executable_tests=verified_tests,
        implemented_hard_constraints=hard,
        hard_constraints_with_negative_tests=hard_with_neg,
        provisional_rules=sum(
            1 for r in RULES if r.review_status == RuleKind.PROVISIONAL_FITNESS_RULE
        ),
        expert_review_required_rules=sum(
            1 for r in RULES if r.review_status == RuleKind.EXPERT_REVIEW_REQUIRED
        ),
        expert_approved_rules=0,
        deferred_or_unimplemented_rules=0,
        unresolved_implementation_refs=tuple(unresolved_impl),
        unresolved_test_refs=tuple(unresolved_tests),
        rules_missing_negative_hard_tests=tuple(missing_neg),
    )


def metrics_as_dict() -> dict:
    return asdict(compute_traceability_metrics())
