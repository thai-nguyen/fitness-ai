"""Structured memory domain models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any


class MemoryType(str, Enum):
    PREFERRED_TRAINING_DAYS = "preferred_training_days"
    PREFERRED_SESSION_DURATION = "preferred_session_duration_minutes"
    PREFERRED_ENVIRONMENT = "preferred_training_environment"
    AVAILABLE_EQUIPMENT = "available_equipment"
    EXERCISE_PREFERENCE = "exercise_preference"


class MemorySourceType(str, Enum):
    EXPLICIT_USER = "explicit_user"
    SYSTEM = "system"


class MemoryStatus(str, Enum):
    ACTIVE = "active"
    DELETED = "deleted"


ALLOWED_MEMORY_TYPES = frozenset(MemoryType)


@dataclass(frozen=True)
class MemoryRecord:
    memory_id: str
    user_id: str
    memory_type: MemoryType
    key: str
    typed_value: Any
    source_reference: str
    source_type: MemorySourceType
    verification_status: str
    status: MemoryStatus
    created_at: datetime
    updated_at: datetime
    version: int
