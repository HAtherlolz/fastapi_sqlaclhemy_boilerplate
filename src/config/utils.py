from typing import TYPE_CHECKING
from urllib.parse import unquote

from sqlalchemy.engine import URL

from src.constants import SQLALCHEMY_POSTGRES_DRIVER_NAME


if TYPE_CHECKING:
    # With TYPE_CHECKING is often the best compromise when dealing with potential circular imports
    # while still maintaining proper type checking.
    # This approach imports DatabaseSettings only during type checking but not at runtime,
    # avoiding potential circular imports.

    from src.config.config import DatabaseSettings


class ConnectionURLFactory:
    """Factory for creating different types of database connection URLs."""

    @staticmethod
    def create_password_auth_url(db_settings: "DatabaseSettings") -> str:
        """Create URL for password authentication"""
        kwargs = {
            "username": db_settings.username,
            "password": db_settings.password,
            "host": db_settings.host,
            "port": db_settings.port,
            "database": db_settings.database,
        }

        if db_settings.engine == "postgres":
            kwargs["drivername"] = SQLALCHEMY_POSTGRES_DRIVER_NAME

        url = URL.create(**kwargs)  # type: ignore
        return unquote(url.render_as_string(hide_password=False))
