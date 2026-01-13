# app/models/user.py
from __future__ import annotations

from sqlalchemy import Boolean, DateTime, String, func, text
from sqlmodel import Field

from src.models.base import BaseSQLModel


class User(BaseSQLModel, table=True):
    """
    Users model.
    """
    __tablename__ = "users"

    email: str = Field(
        sa_type=String(255),  # type: ignore
        unique=True,
        index=True,
        nullable=False,
    )
    hashed_password: str = Field(
        sa_type=String(255),  # type: ignore
        nullable=False,
    )
    first_name: str = Field(
        sa_type=String(255),  # type: ignore
        nullable=False,
    )
    last_name: str = Field(
        sa_type=String(255),  # type: ignore
        nullable=False,
    )

    is_active: bool = Field(
        sa_type=Boolean,
        sa_column_kwargs={
            "server_default": text("true"),
            "nullable": False,
        },
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r})"
