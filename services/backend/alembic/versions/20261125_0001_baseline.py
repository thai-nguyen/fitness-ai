"""Empty baseline migration — verifies Alembic lifecycle (no domain tables).

Revision ID: 20261125_0001
Revises:
Create Date: 2026-11-25

"""

from typing import Sequence, Union

revision: str = "20261125_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Intentionally empty: M03 validates tooling only. Domain schema starts later.
    pass


def downgrade() -> None:
    pass
