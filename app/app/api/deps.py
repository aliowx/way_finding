import logging
from typing import AsyncGenerator

import redis.asyncio as redis
from fastapi import Depends, Request, Response
from redis.asyncio import client
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app import exceptions as exc
from app import models, schemas, utils
from app.core.config import (
    settings,
    ACCESS_TOKEN_BLOCKLIST_KEY,
    REFRESH_TOKEN_BLOCKLIST_KEY,
)
from app.core.security import JWTHandler
from app.db.session import async_session

logger = logging.getLogger(__name__)


async def get_db_async() -> AsyncGenerator:
    """
    Dependency function for get database
    """
    async with async_session() as session:
        yield session


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


async def get_user_id_from_cookie(
    request: Request,
    response: Response,
    cache: client.Redis = Depends(get_redis),
):
    try:
        access_token = request.cookies.get("Access-Token")
        if not access_token:
            raise exc.UnauthorizedException(
                detail="Access-Token is not provided",
                msg_code=utils.MessageCodes.access_token_not_found,
            )

        token = JWTHandler.decode(access_token)
        if await cache.get(ACCESS_TOKEN_BLOCKLIST_KEY.format(token=access_token)):
            raise exc.UnauthorizedException(
                detail="Token expired",
                msg_code=utils.MessageCodes.expired_token,
            )

        user_id = token.get("id")

        if token.get("sub") != "access" or not user_id:
            raise exc.UnauthorizedException(
                detail="Invalid access token", msg_code=utils.MessageCodes.invalid_token
            )

    except:
        refresh_token = request.cookies.get("Refresh-Token", "")
        refresh_token_data = JWTHandler.decode(refresh_token)

        if (
            await cache.get(REFRESH_TOKEN_BLOCKLIST_KEY.format(token=refresh_token))
            or refresh_token_data.get("sub") != "refresh"
        ):
            raise exc.UnauthorizedException(
                detail="Invalid refresh token",
                msg_code=utils.MessageCodes.invalid_token,
            )

        user_id = refresh_token_data.get("id")

        token = JWTHandler.encode(payload={"sub": "access", "id": user_id})

        response.set_cookie(
            key="Access-Token",
            value=token,
            secure=True,
            httponly=True,
            samesite="strict" if not settings.DEBUG else "none",
            expires=JWTHandler.token_expiration(token),
        )
    request.state.user_id = user_id

    return int(user_id)


async def get_current_user(
    db: AsyncSession = Depends(get_db_async),
    current_user_id: int = Depends(get_user_id_from_cookie),
) -> schemas.User:

    current_user = await crud.user.get(db=db, id_=current_user_id)

    if not current_user:
        exc.NotFoundException(
            detail="User not found", msg_code=utils.MessageCodes.not_found
        )

    return current_user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_active(current_user):
        raise exc.ForbiddenException(
            detail="Permission Error",
            msg_code=utils.MessageCodes.permission_error,
        )
    return current_user


async def get_current_active_superuser(
    current_user: models.User = Depends(get_current_active_user),
) -> models.User:
    if not crud.user.is_superuser(current_user):
        raise exc.ForbiddenException(
            detail="Permission Error",
            msg_code=utils.MessageCodes.permission_error,
        )
    return current_user
