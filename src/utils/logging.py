# app/utils/logging.py
from __future__ import annotations

from contextvars import ContextVar, Token
import logging
import logging.config
import os
from typing import Any, Sequence

import uvicorn.logging

from src.config.config import settings


# -------- trace id context --------
trace_id_var: ContextVar[str] = ContextVar("trace_id", default="undefined")


def set_trace_id(trace_id: str) -> Token[str]:
    """Set Trace ID context variable value."""
    return trace_id_var.set(trace_id)


def get_trace_id() -> str:
    """Get Trace ID context variable value."""
    return trace_id_var.get()


# -------- logging helpers --------
class TraceIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.trace_id = get_trace_id()
        return True


class SingleLineFormatter(uvicorn.logging.DefaultFormatter):
    def format(self, record: logging.LogRecord) -> str:
        res = super().format(record).replace("\n", r"\n")
        return res


class LoggingConfig:
    DEFAULT_LOG_FORMAT: str = (
        "[%(trace_id)s] - [%(levelname)s] - %(message)s"
        if os.environ.get("LOG_MODE") == "dev"
        else '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "body": "%(message)s", '
        '"log.logger": "%(name)s", "metadata": {"process": "%(process)d", "path": "%(pathname)s", '
        '"trace_id": "%(trace_id)s"}}'
    )
    DEFAULT_LOG_LEVEL: str = "INFO"

    LOG_FORMAT: str = getattr(settings, "LOG_FORMAT", None) or os.environ.get("LOG_FORMAT") or DEFAULT_LOG_FORMAT
    LOG_LEVEL: str = getattr(settings, "LOG_LEVEL", None) or os.environ.get("LOG_LEVEL") or DEFAULT_LOG_LEVEL
    LOG_MULTILINE_MODE_ENABLED: bool = os.environ.get("LOG_MODE") == "dev"

    LOGGING_CONFIG: dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "logging.Formatter",
                "fmt": LOG_FORMAT,
            },
            "single_line": {
                "()": (SingleLineFormatter if not LOG_MULTILINE_MODE_ENABLED else "logging.Formatter"),
                "fmt": LOG_FORMAT,
            },
        },
        "filters": {"trace_id": {"()": TraceIdFilter}},
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "filters": ["trace_id"],
            },
            "console_single_line": {
                "class": "logging.StreamHandler",
                "formatter": "single_line",
                "filters": ["trace_id"],
            },
        },
        "root": {"handlers": ["console"], "level": LOG_LEVEL},
        "loggers": {
            "app": {
                "handlers": ["console"],
                "level": LOG_LEVEL,
                "propagate": False,
            },
            "app-ml": {
                "handlers": ["console_single_line"],
                "level": LOG_LEVEL,
                "propagate": False,
            },
            "uvicorn": {
                "handlers": ["console"],
                "level": LOG_LEVEL,
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["console"],
                "level": LOG_LEVEL,
                "propagate": False,
            },
            "uvicorn.error": {
                "handlers": ["console"],
                "level": LOG_LEVEL,
                "propagate": False,
            },
            "openai": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
            "httpx": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
            "msgraph": {
                "handlers": ["console"],
                "level": LOG_LEVEL,
                "propagate": False,
            },
            "httpcore": {
                "handlers": ["console"],
                "level": LOG_LEVEL,
                "propagate": False,
            },
        },
    }

    @classmethod
    def configure_logging(cls) -> None:
        logging.config.dictConfig(cls.LOGGING_CONFIG)


def configure_logging() -> None:
    LoggingConfig.configure_logging()


logger = logging.getLogger("app")
multiline_logger = logging.getLogger("app-ml")


def log_messages(title: str, messages: Sequence[Any]) -> None:
    """Dev helper to log list of messages in multiline mode."""
    if os.getenv("LOG_MODE") == "dev":
        multiline_logger.info("===================")
        multiline_logger.info(" -- %s: ", title)
        for message in messages:
            try:
                message_dict = message.dict()  # pydantic BaseModel
            except AttributeError:
                try:
                    message_dict = dict(message)  # mapping-like
                except Exception:
                    message_dict = {"value": repr(message)}
            multiline_logger.info(" ---- %s", message_dict)
        multiline_logger.info("===================")


def log_response(deployment: str, response: Any) -> None:
    if os.getenv("LOG_MODE") == "dev":
        multiline_logger.info("===================")
        multiline_logger.info(" -- %s response: ", deployment)
        multiline_logger.info(" ---- %s", response)
        multiline_logger.info("===================")


def dev_log(title: str, message: Any) -> None:
    if os.getenv("LOG_MODE") == "dev":
        multiline_logger.info("===================")
        multiline_logger.info(" -- %s: ", title)
        multiline_logger.info(" ---- %s", message)
        multiline_logger.info("===================")


configure_logging()
