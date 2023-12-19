from typing import AsyncGenerator

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, exceptions
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, exceptions as exc, models, schemas, utils
from app.core import security
from app.core.config import settings
from app.db.session import async_session

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/users/login/access-token", auto_error=False
)


async def get_db_async() -> AsyncGenerator:
    async with async_session() as session:
        yield session


async def get_current_user(
    db: AsyncSession = Depends(get_db_async), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        if token is None:
            raise exc.UnauthorizedException(
                msg_code=utils.MessageCodes.not_authorized,
                detail="Not Authorized"
            )

        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)

    except (jwt.JWTError, ValidationError, exceptions.ExpiredSignatureError):
        raise exc.ForbiddenException(
            msg_code=utils.MessageCodes.bad_request,
            detail="Could not validate credentials",
        )

    user = await crud.user.get(db, id=int(token_data.sub))
    if not user:
        raise exc.NotFoundException(
            detail="The user with this username does not exist in the system",
            msg_code=utils.MessageCodes.not_found,
        )

    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_active(current_user):
        raise exc.ValidationException(
            detail="Incorrect username or password",
            msg_code=utils.MessageCodes.incorrect_email_or_password,
        )
    return current_user


async def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_superuser(current_user):
        raise exc.ForbiddenException(
            detail="Permission Error",
            msg_code=utils.MessageCodes.permisionError,
        )
    return current_user
