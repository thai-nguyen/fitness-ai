"""Alembic smoke test against disposable project database."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

from tests.conftest import DEFAULT_TEST_DB, database_reachable

BACKEND_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.integration
def test_alembic_upgrade_head() -> None:
    url = os.environ.get("DATABASE_URL", DEFAULT_TEST_DB)
    if not database_reachable(url):
        pytest.skip("PostgreSQL not reachable for migration smoke test")

    env = os.environ.copy()
    env["DATABASE_URL"] = url
    result = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        cwd=BACKEND_ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr + result.stdout

    current = subprocess.run(
        [sys.executable, "-m", "alembic", "current"],
        cwd=BACKEND_ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert current.returncode == 0
    assert "20261125_0001" in current.stdout
