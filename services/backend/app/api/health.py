"""Foundation health endpoints."""

from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, Request, Response, status
from pydantic import BaseModel, Field

from app.core.database import check_database

router = APIRouter(tags=["health"])


class LiveResponse(BaseModel):
    status: Literal["ok"] = "ok"
    service: str
    version: str


class ReadyChecks(BaseModel):
    database: Literal["up", "down"]


class ReadyResponse(BaseModel):
    status: Literal["ready", "not_ready"]
    service: str
    version: str
    checks: ReadyChecks = Field(...)


class VersionResponse(BaseModel):
    service: str
    version: str
    environment: str


@router.get("/health/live", response_model=LiveResponse)
def live(request: Request) -> LiveResponse:
    settings = request.app.state.settings
    return LiveResponse(service=settings.app_name, version=settings.app_version)


@router.get("/health/ready", response_model=ReadyResponse)
def ready(request: Request, response: Response) -> ReadyResponse:
    settings = request.app.state.settings
    db_status: Literal["up", "down"] = "down"
    try:
        check_database()
        db_status = "up"
    except Exception:
        db_status = "down"

    payload = ReadyResponse(
        status="ready" if db_status == "up" else "not_ready",
        service=settings.app_name,
        version=settings.app_version,
        checks=ReadyChecks(database=db_status),
    )
    if payload.status != "ready":
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return payload


@router.get("/version", response_model=VersionResponse)
def version(request: Request) -> VersionResponse:
    settings = request.app.state.settings
    return VersionResponse(
        service=settings.app_name,
        version=settings.app_version,
        environment=settings.app_env,
    )
