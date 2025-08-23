import logging
import logging.config
import os
from contextvars import ContextVar, Token

import uvicorn.logging

from src.settings import settings

trace_id_var: ContextVar[str] = ContextVar("trace_id", default="undefined")


def set_trace_id(trace_id: str) -> Token[str]:
    """Set Trace ID context variable value."""
    return trace_id_var.set(trace_id)


def get_trace_id() -> str:
    """Get Trace ID context variable value."""
    return trace_id_var.get("undefined")


class TraceIdFilter(logging.Filter):
    def filter(self, record):
        record.trace_id = get_trace_id()
        return True


class SingleLineFormatter(uvicorn.logging.DefaultFormatter):
    def format(self, record):
        res = super().format(record).replace("\n", r"\n")
        return res


class LoggingConfig:
    DEFAULT_LOG_FORMAT = (
        "[%(trace_id)s] - [%(levelname)s] - %(message)s"
        if os.environ.get("LOG_MODE") == "dev"
        else '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "body": "%(message)s", "log.logger": "%(name)s", "metadata": {"process": "%(process)d", "path": "%(pathname)s", "trace_id": "%(trace_id)s"}}'
    )

    DEFAULT_LOG_LEVEL = "INFO"

    LOG_FORMAT = settings.log_format or DEFAULT_LOG_FORMAT
    print(f"{LOG_FORMAT=}")

    LOG_LEVEL = settings.log_level or DEFAULT_LOG_LEVEL
    print(f"{LOG_LEVEL=}")

    LOG_MULTILINE_MODE_ENABLED = False
    print(f"{LOG_MULTILINE_MODE_ENABLED=}")

    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "logging.Formatter",
                "fmt": LOG_FORMAT,
            },
            "single_line": {
                # single_line formatter will behave like default if LOG_MULTILINE_LOG_ENABLED
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
        "root": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
        },
        "loggers": {
            "chat-hub": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
            "chat-hub-ml": {  # chat-hub multiline logger
                "handlers": ["console_single_line"],
                "level": LOG_LEVEL,
                "propagate": False,
            },
            # override third-party libs log format
            "uvicorn": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
            "uvicorn.access": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
            "uvicorn.error": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
            "openai": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
            "httpx": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
            "msgraph": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
            "httpcore": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False}
        },
    }

    @classmethod
    def configure_logging(cls):
        logging.config.dictConfig(cls.LOGGING_CONFIG)


def configure_logging():
    LoggingConfig.configure_logging()


ogger = logging.getLogger("app")
multiline_logger = logging.getLogger("app-ml")


def log_messages(title: str, messages: list):
    if os.getenv("LOG_MODE") == "dev":
        multiline_logger.info("===================")
        multiline_logger.info(f" -- {title}: ")
        for message in messages:
            message_dict = message.dict()
            content = message_dict.pop("content")
            message_dict["content"] = content
            multiline_logger.info(f" ---- {message_dict}")
        multiline_logger.info("===================")


def log_response(deployment, response):
    if os.getenv("LOG_MODE") == "dev":
        multiline_logger.info("===================")
        multiline_logger.info(f" -- {deployment} response: ")
        multiline_logger.info(f" ---- {response}")
        multiline_logger.info("===================")


def dev_log(title, message):
    if os.getenv("LOG_MODE") == "dev":
        multiline_logger.info("===================")
        multiline_logger.info(f" -- {title}: ")
        multiline_logger.info(f" ---- {message}")
        multiline_logger.info("===================")


configure_logging()