"""API health endpoint tests."""

from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient

from tests.conftest import DEFAULT_TEST_DB, database_reachable


def test_live(client: TestClient) -> None:
    response = client.get("/health/live")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"] == "fitness-ai-backend"
    assert body["version"] == "0.1.0"


def test_version(client: TestClient) -> None:
    response = client.get("/version")
    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "fitness-ai-backend"
    assert body["environment"] == "test"


@pytest.mark.integration
def test_ready_with_database(client: TestClient) -> None:
    url = os.environ.get("DATABASE_URL", DEFAULT_TEST_DB)
    if not database_reachable(url):
        pytest.skip("PostgreSQL not reachable for integration test")
    response = client.get("/health/ready")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ready"
    assert body["checks"]["database"] == "up"


def test_ready_unavailable_database(unavailable_db_client: TestClient) -> None:
    response = unavailable_db_client.get("/health/ready")
    assert response.status_code == 503
    body = response.json()
    assert body["status"] == "not_ready"
    assert body["checks"]["database"] == "down"


def test_error_schema_does_not_leak_internals(client: TestClient) -> None:
    # Unknown route → FastAPI 404 JSON without stack traces / paths beyond URL.
    response = client.get("/does-not-exist")
    assert response.status_code == 404
    assert "traceback" not in response.text.lower()
