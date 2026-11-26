"""synthetic_ai_memory POC table for PH00-M05

Revision ID: 20261126_0002
Revises: 20261125_0001
Create Date: 2026-11-26
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20261126_0002"
down_revision: str | None = "20261125_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "synthetic_ai_memory",
        sa.Column("memory_id", sa.String(length=64), primary_key=True),
        sa.Column("user_id", sa.String(length=128), nullable=False),
        sa.Column("memory_type", sa.String(length=64), nullable=False),
        sa.Column("key", sa.String(length=128), nullable=False),
        sa.Column("typed_value", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("source_reference", sa.String(length=256), nullable=False),
        sa.Column("source_type", sa.String(length=64), nullable=False),
        sa.Column("verification_status", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
    )
    op.create_index("ix_synthetic_ai_memory_user_id", "synthetic_ai_memory", ["user_id"])
    op.create_index("ix_synthetic_ai_memory_status", "synthetic_ai_memory", ["status"])


def downgrade() -> None:
    op.drop_index("ix_synthetic_ai_memory_status", table_name="synthetic_ai_memory")
    op.drop_index("ix_synthetic_ai_memory_user_id", table_name="synthetic_ai_memory")
    op.drop_table("synthetic_ai_memory")
