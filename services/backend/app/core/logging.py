"""Minimal structured logging using the standard library."""

from __future__ import annotations

import logging
import sys
from typing import Any


class StructuredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        service = getattr(record, "service", "fitness-ai-backend")
        request_id = getattr(record, "request_id", "-")
        base = (
            f"ts={self.formatTime(record, self.datefmt)} "
            f"level={record.levelname} "
            f"service={service} "
            f"request_id={request_id} "
            f"msg={record.getMessage()}"
        )
        if record.exc_info:
            base = f"{base} exc={self.formatException(record.exc_info)}"
        return base


def configure_logging(level: str = "INFO", service_name: str = "fitness-ai-backend") -> None:
    root = logging.getLogger()
    root.handlers.clear()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(StructuredFormatter(datefmt="%Y-%m-%dT%H:%M:%S%z"))
    root.addHandler(handler)
    root.setLevel(getattr(logging, level.upper(), logging.INFO))
    logging.LoggerAdapter(root, {"service": service_name})


def get_logger(name: str, **extra: Any) -> logging.LoggerAdapter[logging.Logger]:
    return logging.LoggerAdapter(logging.getLogger(name), extra)
