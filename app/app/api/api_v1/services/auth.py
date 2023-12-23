import asyncio

from redis.asyncio import client
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app import exceptions as exc
from app import schemas, utils
from app.core.config import REFRESH_TOKEN_KEY, SESSION_ID_KEY, settings
from app.core.security import JWTHandler


async def register(db: AsyncSession, user_in: schemas.UserCreate) -> schemas.User:
    user = await crud.user.get_by_email(db=db, email=user_in.email)
    if user:
        raise exc.AlreadyExistException(
            detail="The user with this username already exists",
            msg_code=utils.MessageCodes.bad_request,
        )
    user = await crud.user.create(db=db, obj_in=user_in)
    return user


async def login(
    db: AsyncSession, user_in: schemas.LoginUser, cache: client.Redis
) -> schemas.Token:
    if not cache:
        raise exc.InternalErrorException(
            detail="Redis connection is not initialized",
            msg_code=utils.MessageCodes.internal_error,
        )
    user = await crud.user.authenticate(
        db=db, email=user_in.email, password=user_in.password
    )
    if not user:
        raise exc.NotFoundException(
            detail="Incorrect email or password",
            msg_code=utils.MessageCodes.incorrect_email_or_password,
        )

    refresh_token = JWTHandler.encode_refresh_token(
        payload={"sub": "refresh_token", "verify": str(user.id)}
    )
    access_token = JWTHandler.encode(payload={"user_id": str(user.id)})
    csrf_token = JWTHandler.encode_refresh_token(
        payload={
            "sub": "csrf_token",
            "refresh_token": str(refresh_token),
            "access_token": str(access_token),
        }
    )
    key = REFRESH_TOKEN_KEY.format(token=refresh_token)
    await cache.set(name=key, value=user.id, ex=JWTHandler.refresh_token_expire)
    return schemas.Token(
        access_token=access_token,
        refresh_token=refresh_token,
        csrf_token=csrf_token,
    )


async def logout(refresh_token: str, cache: client.Redis) -> None:
    if not cache:
        raise exc.InternalErrorException(
            detail="Redis connection is not initialized",
            msg_code=utils.MessageCodes.internal_error,
        )
    if not refresh_token:
        raise exc.NotFoundException(
            detail="Refresh token not found",
            msg_code=utils.MessageCodes.refresh_token_not_found,
        )
    key = REFRESH_TOKEN_KEY.format(token=refresh_token)
    await cache.delete(key)
    return None


async def me(db: AsyncSession, user_in: schemas.LoginUser) -> schemas.User:
    user = await crud.user.authenticate(
        db=db, email=user_in.email, password=user_in.password
    )
    if not user:
        raise exc.NotFoundException(
            detail="Incorrect email or password",
            msg_code=utils.MessageCodes.incorrect_email_or_password,
        )
    return user


async def verify(
    db: AsyncSession,
    cache: client.Redis,
    refresh_token: str,
    session_id: str,
) -> None:
    if not cache:
        raise exc.InternalErrorException(
            detail="Redis connection is not initialized",
            msg_code=utils.MessageCodes.internal_error,
        )
    session_id_key = SESSION_ID_KEY.format(token=session_id)
    refresh_token_key = REFRESH_TOKEN_KEY.format(token=refresh_token)
    session_id_redis, user_id = await asyncio.gather(
        cache.get(session_id_key), cache.get(refresh_token_key)
    )
    if not user_id:
        raise exc.UnauthorizedException(
            detail="Invalid refresh token", msg_code=utils.MessageCodes.invalid_token
        )
    elif not session_id_redis:
        user = await crud.user.get(db=db, id=int(user_id))
        if not user:
            raise exc.NotFoundException(
                detail="User not found", msg_code=utils.MessageCodes.not_found
            )
        await cache.set(
            name=session_id_key, value=user_id, ex=settings.SESSION_EXPIRE_MINUTES * 60
        )
    else:
        raise exc.ValidationException(
            detail="Already verified", msg_code=utils.MessageCodes.already_verifide
        )
    return None


async def refresh_token(old_refresh_token: str, cache: client.Redis) -> schemas.Token:
    if not cache:
        raise exc.InternalErrorException(
            detail="Redis connection is not initialized",
            msg_code=utils.MessageCodes.internal_error,
        )
    old_key = REFRESH_TOKEN_KEY.format(token=old_refresh_token)
    user_id, ttl = await asyncio.gather(cache.get(old_key), cache.ttl(old_key))
    if not user_id:
        exc.UnauthorizedException(
            detail="Invalid token", msg_code=utils.MessageCodes.invalid_token
        )

    access_token = JWTHandler.encode(payload={"user_id": str(user_id)})
    refresh_token = JWTHandler.encode_refresh_token(
        payload={"sub": "refresh_token", "verify": str(user_id)}
    )
    csrf_token = JWTHandler.encode_refresh_token(
        payload={
            "sub": "csrf_token",
            "refresh_token": str(refresh_token),
            "access_token": str(access_token),
        }
    )
    key = REFRESH_TOKEN_KEY.format(token=refresh_token)
    await asyncio.gather(
        cache.set(name=key, value=user_id, ex=ttl), cache.delete(old_key)
    )
    return schemas.Token(
        access_token=access_token, refresh_token=refresh_token, csrf_token=csrf_token
    )
