from typing import Any

from pydantic import AnyHttpUrl, EmailStr, PostgresDsn, RedisDsn, field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

REFRESH_TOKEN_KEY = "refresh_token:{token}"
SESSION_ID_KEY = "session_id:{token}"


class AsyncPostgresDsn(PostgresDsn):
    allowed_schemes = {"postgres+asyncpg", "postgresql+asyncpg"}


class Settings(BaseSettings):
    PROJECT_NAME: str
    API_V1_STR: str = "/api/v1"

    DEBUG: bool = False
    SECRET_KEY: str
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] | str = []

    # 60 minutes * 24 hours * 1 day = 1 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    SESSION_EXPIRE_MINUTES: int
    JWT_ALGORITHM: str = "HS256"

    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int
    SQLALCHEMY_DATABASE_ASYNC_URI: AsyncPostgresDsn | None = None

    RABBITMQ_USERNAME: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: str

    REDIS_SERVER: str
    REDIS_PORT: int
    REDIS_DATABASE: int = 0
    REDIS_USERNAME: str = ""
    REDIS_PASSWORD: str
    REDIS_TIMEOUT: int | None = 5
    REDIS_URI: RedisDsn | None = None

    @classmethod
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str):
            return [i.strip() for i in v.strip("[]").split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @property
    def allow_origins(self) -> list[str]:
        return [str(origin).strip("/") for origin in self.BACKEND_CORS_ORIGINS]

    @field_validator("SQLALCHEMY_DATABASE_ASYNC_URI", mode="before")
    def assemble_async_db_connection(cls, v: str | None, values: Any) -> Any:
        if isinstance(v, str):
            return v
        return AsyncPostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.data.get("POSTGRES_USER"),
            password=values.data.get("POSTGRES_PASSWORD"),
            host=values.data.get("POSTGRES_SERVER"),
            port=values.data.get("POSTGRES_PORT"),
            path=f"{values.data.get('POSTGRES_DB') or ''}",
        )

    @field_validator("REDIS_URI", mode="before")
    @classmethod
    def assemble_redis_URI_connection(
        cls, v: str | None, values: ValidationInfo
    ) -> Any:
        if isinstance(v, str):
            return v
        return RedisDsn.build(
            scheme="redis",
            username=values.data.get("REDIS_USERNAME"),
            password=values.data.get("REDIS_PASSWORD"),
            host=values.data.get("REDIS_SERVER"),
            port=values.data.get("REDIS_PORT"),
            path=f"{values.data.get('REDIS_DATABASE') or ''}",
        )

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
