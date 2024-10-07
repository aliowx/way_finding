from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.models.user import User
from app.schemas.user import UserCreate
from tests.utils.utils import random_email, random_lower_string


async def create_random_user(db: AsyncSession) -> User:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(username=email, email=email, password=password)
    user = await crud.user.create(db=db, obj_in=user_in)
    return user
