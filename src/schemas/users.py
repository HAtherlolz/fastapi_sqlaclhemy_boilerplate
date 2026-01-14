"""
The schemas for users request, request
"""

from datetime import datetime
import re

from pydantic import BaseModel, field_validator


class UserCreateRequestSchema(BaseModel):
    """
    Request schema for user creation.
    """

    email: str
    password: str
    full_name: str

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        value = value.strip()

        # exactly two words, only letters
        if not re.fullmatch(r"[A-Za-z]+(?:\s+[A-Za-z]+)", value):
            raise ValueError("full_name must consist of exactly two words containing only letters")

        return value


class UserDetailSchema(BaseModel):
    """
    User detail schema for retrieving.
    """

    email: str
    first_name: str
    last_name: str
    is_active: bool
    created_at: datetime


class UserLoginRequestSchema(BaseModel):
    email: str
    password: str


class RefreshTokenRequestSchema(BaseModel):
    refresh_token: str


class UserJwtSchema(RefreshTokenRequestSchema):
    access_token: str
