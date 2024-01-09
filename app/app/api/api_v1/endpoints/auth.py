import asyncio
import time

from fastapi import APIRouter, Depends, Request, Response
from redis.asyncio import client
from sqlalchemy.ext.asyncio import AsyncSession

from app import exceptions as exc
from app import schemas, utils
from app.api import deps
from app.api.api_v1 import services
from app.core.security import JWTHandler
from app.utils import APIResponse, APIResponseType

router = APIRouter()


@router.post("/login")
async def login(
    response: Response,
    user_in: schemas.LoginUser,
    db: AsyncSession = Depends(deps.get_db_async),
    cache: client.Redis = Depends(deps.get_redis),
) -> APIResponseType[schemas.Msg]:
    """Login"""
    start_time = time.time()
    try:
        tokens = await services.login(db=db, user_in=user_in, cache=cache)
        elapsed_time = time.time() - start_time
        if elapsed_time < 1:
            await asyncio.sleep(1 - elapsed_time)
    except Exception as e:
        end_time = time.time()
        elapsed_time = end_time - start_time
        if elapsed_time < 1:
            await asyncio.sleep(1 - elapsed_time)
        raise e from None

    response.set_cookie(
        key="Refresh-Token",
        value=tokens.refresh_token,
        secure=True,
        httponly=True,
        samesite="strict",
        expires=JWTHandler.token_expiration(tokens.refresh_token),
    )
    response.set_cookie(
        key="Access-Token",
        value=tokens.access_token,
        secure=True,
        httponly=True,
        samesite="strict",
        expires=JWTHandler.token_expiration(tokens.access_token),
    )
    response.headers["X-CSRF-TOKEN"] = tokens.csrf_token

    return APIResponse(schemas.Msg(msg="You have successfully logged in"))


@router.post("/refresh")
async def refresh_token(
    request: Request,
    response: Response,
    user_id: str = Depends(deps.get_current_user_with_refresh),
    cache: client.Redis = Depends(deps.get_redis),
) -> None:
    """Refresh token"""
    if not user_id:
        raise exc.NotFoundException(
            detail="User not found", msg_code=utils.MessageCodes.not_found
        )
    start_time = time.time()
    try:
        tokens = await services.refresh_token(
            old_refresh_token=request.cookies.get("Refresh-Token", ""), cache=cache
        )
        elapsed_time = time.time() - start_time
        if elapsed_time < 1:
            await asyncio.sleep(1 - elapsed_time)
    except Exception as e:
        end_time = time.time()
        elapsed_time = end_time - start_time
        if elapsed_time < 1:
            await asyncio.sleep(1 - elapsed_time)
        raise e from None

    if not tokens.access_token:
        raise exc.NotFoundException(
            detail="Access token not found",
            msg_code=utils.MessageCodes.not_found,
        )
    response.set_cookie(
        key="Refresh-Token",
        value=tokens.refresh_token,
        secure=True,
        httponly=True,
        samesite="strict",
        expires=JWTHandler.token_expiration(tokens.refresh_token),
    )
    response.set_cookie(
        key="Access-Token",
        value=tokens.access_token,
        secure=True,
        httponly=True,
        samesite="strict",
        expires=JWTHandler.token_expiration(tokens.access_token),
    )
    response.headers["X-CSRF-TOKEN"] = tokens.csrf_token


@router.post("/verify")
async def verify(
    request: Request,
    db: AsyncSession = Depends(deps.get_db_async),
    user_id: str = Depends(deps.get_current_user_with_refresh),
    cache: client.Redis = Depends(deps.get_redis),
) -> None:
    """Verify"""
    if not user_id:
        raise exc.NotFoundException(
            detail="User not found", msg_code=utils.MessageCodes.not_found
        )
    await services.verify(
        db=db,
        refresh_token=request.cookies.get("Refresh-Token", ""),
        session_id=request.cookies.get("Session-Id", ""),
        cache=cache,
    )


@router.post("/register")
async def register(
    user_in: schemas.UserCreate, db: AsyncSession = Depends(deps.get_db_async)
) -> APIResponseType[schemas.User]:
    """Register new user"""
    response = await services.register(db=db, user_in=user_in)
    return APIResponse(response)


@router.get("/me")
async def me(
    current_user: schemas.User = Depends(deps.get_current_user),
) -> APIResponseType[schemas.User]:
    """Retrieve current user"""
    return APIResponse(current_user)


@router.delete("/logout")
async def logout(
    request: Request,
    response: Response,
    current_user: schemas.User = Depends(deps.get_current_user),
    cache: client.Redis = Depends(deps.get_redis),
) -> APIResponseType[schemas.Msg]:
    """Logout from system"""
    await services.logout(
        refresh_token=request.cookies.get("Refresh-Token", ""), cache=cache
    )
    response.delete_cookie(
        key="Refresh-Token",
        secure=True,
        httponly=True,
        samesite="strict",
    )
    response.delete_cookie(
        key="Access-Token",
        secure=True,
        httponly=True,
        samesite="strict",
    )
    return APIResponse(schemas.Msg(msg="You have successfully logged out"))
