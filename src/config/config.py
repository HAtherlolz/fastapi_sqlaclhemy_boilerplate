import os
from typing import Literal

from dotenv import load_dotenv
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.config.utils import ConnectionURLFactory


load_dotenv()


ENV_FILE_MODEL_CONFIG = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    extra="ignore",
)


class Settings(BaseSettings):
    model_config = ENV_FILE_MODEL_CONFIG

    # SMTP settings
    MAIL_USERNAME: str | None = None
    MAIL_PASSWORD: str | None = None
    EMAILS_FROM_NAME: str | None = None
    MAIL_FROM: str | None = None
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_STARTTLS: bool = False
    MAIL_SSL_TLS: bool = True
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    # Project name
    PROJECT_NAME: str | None = None

    # Swagger
    SWAGGER_URL: str | None = None

    # Domain
    DOMAIN: str | None = None

    # DB Connection
    DB_ENGINE: Literal["postgres", "mssql"] = "postgres"
    DB_PASSWORD_AUTH: bool = True
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_DATABASE: str

    # Jwt
    SECRET_KEY: str | None = None
    ALGORITHM: str | None = None
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    # Allowed hosts
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8080",
    ]

    @computed_field(return_type=str)
    def DB_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USERNAME}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"
        )

    @computed_field(return_type=dict[str, str])
    def DB_URL_DICT_ALEMBIC(self) -> dict[str, str]:
        return {
            "sqlalchemy.url": (
                f"postgresql://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"
            )
        }


class DatabaseSettings(BaseSettings):
    model_config = ENV_FILE_MODEL_CONFIG | SettingsConfigDict(env_prefix="DB_")
    engine: Literal["postgres", "mssql"] = "postgres"
    password_auth: bool = False
    username: str | None = None
    password: str | None = None

    host: str
    port: int
    database: str

    # pool settings
    pool_size: int = 10
    pool_pre_ping: bool = True
    pool_recycle: int = 1500

    @computed_field  # type: ignore
    @property
    def echo(self) -> bool:
        return os.environ.get("ENV", "").lower() == "dev"

    @computed_field  # type: ignore
    @property
    def connection_url(self) -> str:
        """Generate connection URL using the appropriate factory method."""
        return ConnectionURLFactory.create_password_auth_url(self)


settings = Settings()  # type: ignore[call-arg]
