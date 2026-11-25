"""FastAPI application factory."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.health import router as health_router
from app.core.config import Settings, clear_settings_cache, get_settings
from app.core.database import dispose_engine, init_engine
from app.core.logging import configure_logging, get_logger


def create_app(settings: Settings | None = None) -> FastAPI:
    clear_settings_cache()
    resolved = settings or get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        configure_logging(resolved.log_level, resolved.app_name)
        log = get_logger("app.startup", service=resolved.app_name)
        init_engine(resolved.database_url, echo=False)
        app.state.settings = resolved
        log.info("application_started env=%s version=%s", resolved.app_env, resolved.app_version)
        try:
            yield
        finally:
            dispose_engine()
            log.info("application_stopped")

    app = FastAPI(
        title=resolved.app_name,
        version=resolved.app_version,
        lifespan=lifespan,
    )
    app.state.settings = resolved
    app.include_router(health_router)

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        log = get_logger("app.errors", service=resolved.app_name)
        log.error("unhandled_error path=%s", request.url.path)
        return JSONResponse(
            status_code=500,
            content={
                "error": "internal_server_error",
                "message": "An unexpected error occurred",
            },
        )

    return app


app = create_app()
