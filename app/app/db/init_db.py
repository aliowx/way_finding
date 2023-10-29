import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.core.config import settings
from app.db import base  # noqa: F401
from app.db.session import async_session

logger = logging.getLogger(__name__)


async def create_super_admin(db: AsyncSession) -> None:
    user = await crud.user.get_by_email(db=db, email=settings.FIRST_SUPERUSER)
    if not user:
        user = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        await crud.user.create(db=db, obj_in=user)


async def init_db(db: AsyncSession) -> None:
    await create_super_admin(db)


if __name__ == "__main__":
    import asyncio
    db = async_session()
    asyncio.run(init_db(db))
