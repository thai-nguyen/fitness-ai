"""Controlled memory application service (no direct LLM DB writes)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from app.modules.ai_memory.domain.models import (
    ALLOWED_MEMORY_TYPES,
    MemoryRecord,
    MemorySourceType,
    MemoryStatus,
    MemoryType,
)


class MemoryError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(message)


@dataclass
class InMemoryStore:
    """Process-local store used for unit tests; SQL store wraps the same API."""

    _rows: dict[str, MemoryRecord]

    def __init__(self) -> None:
        self._rows = {}

    def upsert(self, record: MemoryRecord) -> MemoryRecord:
        self._rows[record.memory_id] = record
        # enforce one active key per user/type/key
        for mid, existing in list(self._rows.items()):
            if (
                mid != record.memory_id
                and existing.user_id == record.user_id
                and existing.memory_type == record.memory_type
                and existing.key == record.key
                and existing.status == MemoryStatus.ACTIVE
            ):
                self._rows[mid] = MemoryRecord(
                    memory_id=existing.memory_id,
                    user_id=existing.user_id,
                    memory_type=existing.memory_type,
                    key=existing.key,
                    typed_value=existing.typed_value,
                    source_reference=existing.source_reference,
                    source_type=existing.source_type,
                    verification_status=existing.verification_status,
                    status=MemoryStatus.DELETED,
                    created_at=existing.created_at,
                    updated_at=datetime.now(UTC),
                    version=existing.version + 1,
                )
        return record

    def list_active(self, user_id: str) -> list[MemoryRecord]:
        return [
            r
            for r in self._rows.values()
            if r.user_id == user_id and r.status == MemoryStatus.ACTIVE
        ]

    def get(self, user_id: str, memory_id: str) -> MemoryRecord | None:
        r = self._rows.get(memory_id)
        if r is None or r.user_id != user_id:
            return None
        return r

    def delete(self, user_id: str, memory_id: str) -> bool:
        r = self.get(user_id, memory_id)
        if r is None or r.status != MemoryStatus.ACTIVE:
            return False
        self._rows[memory_id] = MemoryRecord(
            memory_id=r.memory_id,
            user_id=r.user_id,
            memory_type=r.memory_type,
            key=r.key,
            typed_value=r.typed_value,
            source_reference=r.source_reference,
            source_type=r.source_type,
            verification_status=r.verification_status,
            status=MemoryStatus.DELETED,
            created_at=r.created_at,
            updated_at=datetime.now(UTC),
            version=r.version + 1,
        )
        return True


def validate_memory_value(memory_type: MemoryType, value: Any) -> Any:
    if memory_type == MemoryType.PREFERRED_SESSION_DURATION:
        if not isinstance(value, int) or value < 20 or value > 90:
            raise MemoryError("INVALID_VALUE", "session duration must be 20-90")
        return value
    if memory_type == MemoryType.PREFERRED_ENVIRONMENT:
        if value not in {"home", "gym"}:
            raise MemoryError("INVALID_VALUE", "environment must be home|gym")
        return value
    if memory_type in {
        MemoryType.PREFERRED_TRAINING_DAYS,
        MemoryType.AVAILABLE_EQUIPMENT,
        MemoryType.EXERCISE_PREFERENCE,
    }:
        if not isinstance(value, list) or not all(isinstance(x, str) for x in value):
            raise MemoryError("INVALID_VALUE", "expected list[str]")
        return value
    raise MemoryError("UNSUPPORTED_TYPE", "unsupported memory type")


class MemoryApplicationService:
    def __init__(self, store: InMemoryStore):
        self._store = store

    def propose_and_apply(
        self,
        *,
        trusted_user_id: str,
        memory_type: str,
        key: str,
        value: Any,
        source_reference: str,
        source_type: MemorySourceType = MemorySourceType.EXPLICIT_USER,
    ) -> MemoryRecord:
        if not trusted_user_id.startswith("synth_"):
            raise MemoryError("UNTRUSTED_USER", "only synthetic users allowed in M05")
        try:
            mtype = MemoryType(memory_type)
        except ValueError as exc:
            raise MemoryError("UNSUPPORTED_TYPE", "unsupported memory type") from exc
        if mtype not in ALLOWED_MEMORY_TYPES:
            raise MemoryError("UNSUPPORTED_TYPE", "unsupported memory type")
        # Safety restrictions cannot be removed via ordinary preference update
        if key.lower() in {"safety_restriction", "adult_eligible", "rule_set_version"}:
            raise MemoryError("FORBIDDEN_KEY", "safety fields not writable via memory")
        typed = validate_memory_value(mtype, value)
        now = datetime.now(UTC)
        record = MemoryRecord(
            memory_id=str(uuid4()),
            user_id=trusted_user_id,
            memory_type=mtype,
            key=key,
            typed_value=typed,
            source_reference=source_reference,
            source_type=source_type,
            verification_status="explicit",
            status=MemoryStatus.ACTIVE,
            created_at=now,
            updated_at=now,
            version=1,
        )
        return self._store.upsert(record)

    def list_for_user(self, trusted_user_id: str) -> list[MemoryRecord]:
        return self._store.list_active(trusted_user_id)

    def delete_for_user(self, trusted_user_id: str, memory_id: str) -> bool:
        return self._store.delete(trusted_user_id, memory_id)

    def resolve_conflicts(
        self,
        *,
        authoritative: dict[str, Any],
        memories: list[MemoryRecord],
    ) -> dict[str, Any]:
        """Authoritative domain records override conflicting memory."""
        merged = {m.key: m.typed_value for m in memories}
        merged.update(authoritative)
        return merged
