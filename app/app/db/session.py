from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

engine_async = create_async_engine(
    settings.SQLALCHEMY_DATABASE_ASYNC_URI.unicode_string()
)

async_session = async_sessionmaker(
    bind=engine_async,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)
