import logging
from typing import AsyncGenerator

import redis.asyncio as redis
from fastapi import Depends, Request
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer,
)
from redis.asyncio import client
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app import exceptions as exc
from app import models, schemas, utils
from app.core.config import settings
from app.core.security import JWTHandler
from app.db.session import async_session

logger = logging.getLogger(__name__)
http_bearer = HTTPBearer(auto_error=False)
http_basic = HTTPBasic(auto_error=False)


async def get_db_async() -> AsyncGenerator:
    """
    Dependency function for get database
    """
    async with async_session() as session:
        yield session


async def get_user_from_access_token(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    db: AsyncSession = Depends(get_db_async),
) -> schemas.User:
    if credentials.scheme != "Bearer":
        raise exc.UnauthorizedException(
            detail="Invalid header", msg_code=utils.MessageCodes.invalid_token
        )
    access_token = request.cookies.get("Access-Token")
    if not access_token:
        raise exc.NotFoundException(
            detail="Access-Token is not provided",
            msg_code=utils.MessageCodes.access_token_not_found,
        )
    if not credentials.credentials == access_token:
        raise exc.UnauthorizedException(
            detail="Invalid access token", msg_code=utils.MessageCodes.invalid_token
        )
    token = JWTHandler.decode(access_token)
    user_id = token.get("user_id")
    if not user_id:
        raise exc.UnauthorizedException(
            detail="Invalid access token", msg_code=utils.MessageCodes.invalid_token
        )
    user = await crud.user.get(db=db, id_=int(user_id))
    return user


async def get_current_user(
    request: Request,
    token: HTTPAuthorizationCredentials = Depends(http_bearer),
    credentials: HTTPBasicCredentials = Depends(http_basic),
    db: AsyncSession = Depends(get_db_async),
) -> schemas.User:
    """
    Dependency function for get user with access token
    """
    if not (token or credentials):
        raise exc.NotFoundException(
            detail="Token or username and password not found",
            msg_code=utils.MessageCodes.not_found,
        )
    user = None
    if credentials:
        user = await crud.user.authenticate(
            db=db, email=credentials.username, password=credentials.password
        )
    elif token:
        user = await get_user_from_access_token(
            db=db, credentials=token, request=request
        )

    if not user:
        exc.NotFoundException(
            detail="User not found", msg_code=utils.MessageCodes.not_found
        )

    if not crud.user.is_active(user):
        raise exc.ForbiddenException(
            detail="Inactive user", msg_code=utils.MessageCodes.inactive_user
        )
    return user


async def get_current_user_with_refresh(
    request: Request, credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
) -> schemas.User:
    """
    Dependency function for get user with refresh token
    """
    if credentials.scheme != "Bearer":
        raise exc.UnauthorizedException(
            detail="Invalid header", msg_code=utils.MessageCodes.invalid_token
        )
    refresh_token = request.cookies.get("Refresh-Token")
    if not refresh_token:
        raise exc.NotFoundException(
            detail="Refresh-Token is not provided",
            msg_code=utils.MessageCodes.refresh_token_not_found,
        )
    if not credentials.credentials == refresh_token:
        raise exc.UnauthorizedException(
            detail="Invalid refresh token", msg_code=utils.MessageCodes.invalid_token
        )
    token = JWTHandler.decode(refresh_token)
    user_id = token.get("verify")
    if not user_id:
        raise exc.UnauthorizedException(
            detail="Invalid refresh token", msg_code=utils.MessageCodes.invalid_token
        )
    return user_id


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
            msg_code=utils.MessageCodes.permission_error,
        )
    return current_user


async def get_redis() -> client.Redis:
    """
    Dependency function that get redis client
    """
    redis_url = str(settings.REDIS_URI)
    redis_client = await redis.from_url(redis_url, decode_responses=True)
    try:
        if await redis_client.ping():
            return redis_client
    except Exception as e:
        logger.error(logger.error(f"Redis connection failed\n{e}"))
        raise exc.InternalErrorException(
            msg_code=utils.MessageCodes.operation_failed,
        ) from e
