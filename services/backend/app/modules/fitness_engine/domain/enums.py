"""Controlled vocabularies for fitness engine inputs/outputs."""

from __future__ import annotations

from enum import Enum


class Goal(str, Enum):
    GENERAL_FITNESS = "general_fitness"
    MUSCLE_GAIN = "muscle_gain"
    WEIGHT_LOSS_SUPPORT = "weight_loss_support"
    BEGINNER_STRENGTH = "beginner_strength"


class ExperienceLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class Weekday(str, Enum):
    MON = "mon"
    TUE = "tue"
    WED = "wed"
    THU = "thu"
    FRI = "fri"
    SAT = "sat"
    SUN = "sun"


class RuleKind(str, Enum):
    TECHNICAL_INVARIANT = "TECHNICAL_INVARIANT"
    PROVISIONAL_FITNESS_RULE = "PROVISIONAL_FITNESS_RULE"
    EXPERT_REVIEW_REQUIRED = "EXPERT_REVIEW_REQUIRED"


class SafetyOutcome(str, Enum):
    PASSED_TECHNICAL_CHECKS = "PASSED_TECHNICAL_CHECKS"
    REJECTED = "REJECTED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    INSUFFICIENT_INFORMATION = "INSUFFICIENT_INFORMATION"


class GenerationOutcome(str, Enum):
    VALIDATED_TECHNICAL_DRAFT = "VALIDATED_TECHNICAL_DRAFT"
    INVALID_INPUT = "INVALID_INPUT"
    UNSUPPORTED_PROFILE = "UNSUPPORTED_PROFILE"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    INSUFFICIENT_CATALOG = "INSUFFICIENT_CATALOG"
    INFEASIBLE_CONSTRAINTS = "INFEASIBLE_CONSTRAINTS"
    VALIDATION_FAILED = "VALIDATION_FAILED"


class Severity(str, Enum):
    ERROR = "error"
    WARNING = "warning"
