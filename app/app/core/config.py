from typing import Any, List, Optional, Union

from pydantic import field_validator, AnyHttpUrl, EmailStr, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class AsyncPostgresDsn(PostgresDsn):
    allowed_schemes = {"postgres+asyncpg", "postgresql+asyncpg"}


class Settings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_TEST_DB: str
    POSTGRES_PORT: int
    POSTGRES_TEST_DB: str

    PROJECT_NAME: str
    API_V1_STR: str = "/api/v1"
    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str
    EMAIL_TEST_USER: EmailStr
    DEBUG: bool = False

    USERS_OPEN_REGISTRATION: bool = True
    SECRET_KEY: str
    # 60 minutes * 24 hours * 1 day = 1 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1

    RABBITMQ_USERNAME: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: str

    REDIS_SERVER: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_TIMEOUT: Optional[int] = 5

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] | str = []

    @classmethod
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str):
            return [i.strip() for i in v.strip("[]").split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @property
    def allow_origins(self) -> list[str]:
        return [str(origin).strip("/") for origin in self.BACKEND_CORS_ORIGINS]

    SQLALCHEMY_DATABASE_ASYNC_URI: Optional[AsyncPostgresDsn] = None

    @field_validator("SQLALCHEMY_DATABASE_ASYNC_URI", mode="before")
    def assemble_async_db_connection(cls, v: Optional[str], values: Any) -> Any:
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

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
