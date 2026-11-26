"""Provisional training templates for technical evaluation."""

from __future__ import annotations

from dataclasses import dataclass

from app.modules.exercise_catalog.domain.models import MovementPattern
from app.modules.fitness_engine.domain.enums import ExperienceLevel, Goal


@dataclass(frozen=True)
class MovementSlot:
    slot_id: str
    movement_pattern: MovementPattern
    required: bool = True


@dataclass(frozen=True)
class TrainingTemplate:
    template_id: str
    name: str
    supported_goals: tuple[Goal, ...]
    supported_experience: tuple[ExperienceLevel, ...]
    min_days: int
    max_days: int
    slots: tuple[MovementSlot, ...]
    default_working_sets: int
    rule_version: str
    review_status: str


TEMPLATES: tuple[TrainingTemplate, ...] = (
    TrainingTemplate(
        template_id="tmpl_beginner_full_body",
        name="Beginner full-body",
        supported_goals=(Goal.GENERAL_FITNESS, Goal.BEGINNER_STRENGTH, Goal.WEIGHT_LOSS_SUPPORT),
        supported_experience=(ExperienceLevel.BEGINNER,),
        min_days=2,
        max_days=3,
        slots=(
            MovementSlot("s1", MovementPattern.SQUAT),
            MovementSlot("s2", MovementPattern.PUSH),
            MovementSlot("s3", MovementPattern.PULL),
            MovementSlot("s4", MovementPattern.HINGE),
            MovementSlot("s5", MovementPattern.CORE, required=False),
        ),
        default_working_sets=2,
        rule_version="m04-provisional-1",
        review_status="PROVISIONAL_FITNESS_RULE",
    ),
    TrainingTemplate(
        template_id="tmpl_general_fitness",
        name="General fitness",
        supported_goals=(Goal.GENERAL_FITNESS, Goal.WEIGHT_LOSS_SUPPORT),
        supported_experience=(ExperienceLevel.BEGINNER, ExperienceLevel.INTERMEDIATE),
        min_days=2,
        max_days=4,
        slots=(
            MovementSlot("s1", MovementPattern.SQUAT),
            MovementSlot("s2", MovementPattern.PUSH),
            MovementSlot("s3", MovementPattern.PULL),
            MovementSlot("s4", MovementPattern.CARDIO, required=False),
            MovementSlot("s5", MovementPattern.CORE, required=False),
        ),
        default_working_sets=3,
        rule_version="m04-provisional-1",
        review_status="PROVISIONAL_FITNESS_RULE",
    ),
    TrainingTemplate(
        template_id="tmpl_home_bodyweight",
        name="Home bodyweight",
        supported_goals=(Goal.GENERAL_FITNESS, Goal.WEIGHT_LOSS_SUPPORT, Goal.BEGINNER_STRENGTH),
        supported_experience=(ExperienceLevel.BEGINNER, ExperienceLevel.INTERMEDIATE),
        min_days=2,
        max_days=4,
        slots=(
            MovementSlot("s1", MovementPattern.SQUAT),
            MovementSlot("s2", MovementPattern.PUSH),
            MovementSlot("s3", MovementPattern.HINGE),
            MovementSlot("s4", MovementPattern.CORE),
        ),
        default_working_sets=2,
        rule_version="m04-provisional-1",
        review_status="PROVISIONAL_FITNESS_RULE",
    ),
    TrainingTemplate(
        template_id="tmpl_gym_strength",
        name="Basic gym strength",
        supported_goals=(Goal.MUSCLE_GAIN, Goal.BEGINNER_STRENGTH, Goal.GENERAL_FITNESS),
        supported_experience=(ExperienceLevel.BEGINNER, ExperienceLevel.INTERMEDIATE),
        min_days=3,
        max_days=4,
        slots=(
            MovementSlot("s1", MovementPattern.SQUAT),
            MovementSlot("s2", MovementPattern.HINGE),
            MovementSlot("s3", MovementPattern.PUSH),
            MovementSlot("s4", MovementPattern.PULL),
            MovementSlot("s5", MovementPattern.LUNGE, required=False),
        ),
        default_working_sets=3,
        rule_version="m04-provisional-1",
        review_status="PROVISIONAL_FITNESS_RULE",
    ),
)


def select_template(
    goal: Goal,
    experience: ExperienceLevel,
    available_day_count: int,
    prefers_home: bool,
    prefers_gym: bool,
) -> TrainingTemplate | None:
    """Deterministic template selection with stable priority order."""
    candidates = [
        t
        for t in TEMPLATES
        if goal in t.supported_goals
        and experience in t.supported_experience
        and t.min_days <= available_day_count
    ]
    if not candidates:
        return None

    def rank(t: TrainingTemplate) -> tuple[int, int, str]:
        home_bias = 0 if (prefers_home and t.template_id == "tmpl_home_bodyweight") else 1
        gym_bias = 0 if (prefers_gym and t.template_id == "tmpl_gym_strength") else 1
        # Prefer templates whose max_days is closest but not under available count
        fit = abs(min(available_day_count, t.max_days) - t.min_days)
        return (home_bias if prefers_home else gym_bias if prefers_gym else 1, fit, t.template_id)

    return sorted(candidates, key=rank)[0]
