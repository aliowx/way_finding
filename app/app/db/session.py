from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


engine = create_engine(settings.SQLALCHEMY_DATABASE_URI.unicode_string())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
engine_async = create_async_engine(
    settings.SQLALCHEMY_DATABASE_ASYNC_URI.unicode_string()
)
async_session = sessionmaker(
    bind=engine_async,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)
