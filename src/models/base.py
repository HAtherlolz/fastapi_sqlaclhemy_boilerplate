# src/models/base.py
from datetime import datetime
from typing import ClassVar

from sqlalchemy import DateTime, func
from sqlmodel import Field, SQLModel


class BaseSQLModel(SQLModel):
    abstract: ClassVar[bool] = True

    id: int | None = Field(default=None, primary_key=True)

    created_at: datetime = Field(
        sa_type=DateTime(timezone=True),  # type: ignore
        sa_column_kwargs={
            "server_default": func.now(),
            "nullable": False,
        },
    )

    updated_at: datetime = Field(
        sa_type=DateTime(timezone=True),  # type: ignore
        sa_column_kwargs={
            "server_default": func.now(),
            "onupdate": func.now(),
            "nullable": False,
        },
    )
