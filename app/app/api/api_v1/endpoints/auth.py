import time

from fastapi import APIRouter, Depends, Request, Response
from redis.asyncio import client
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.api.api_v1 import services
from app.core.security import JWTHandler
from app import schemas, models
from app.core.config import settings
from cache import invalidate
from app.utils import APIResponse, APIResponseType
from app.api.api_v1.endpoints.users import namespace as users_namespace

router = APIRouter()


@router.post("/login")
async def login(
    response: Response,
    user_in: schemas.LoginUser,
    db: AsyncSession = Depends(deps.get_db_async),
) -> APIResponseType[schemas.Msg]:
    """Login"""

    tokens = await services.login(db=db, user_in=user_in)

    response.set_cookie(
        key="Refresh-Token",
        value=tokens.refresh_token,
        secure=True,
        httponly=True,
        samesite="strict" if not settings.DEBUG else "none",
        expires=int(JWTHandler.token_expiration(tokens.refresh_token) - time.time()),
    )
    response.set_cookie(
        key="Access-Token",
        value=tokens.access_token,
        secure=True,
        httponly=True,
        samesite="strict" if not settings.DEBUG else "none",
        expires=int(JWTHandler.token_expiration(tokens.access_token) - time.time()),
    )

    return APIResponse(schemas.Msg(msg="You have successfully logged in"))


@router.post("/register")
@invalidate(namespace=users_namespace)
async def register(
    user_in: schemas.UserCreate,
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> APIResponseType[schemas.User]:
    """Register new user"""
    response = await services.register(db=db, user_in=user_in)
    return APIResponse(response)


@router.get("/me")
async def me(
    current_user: schemas.User = Depends(deps.get_current_active_user),
) -> APIResponseType[schemas.User]:
    """Retrieve current user"""
    return APIResponse(current_user)


@router.delete("/logout")
async def logout(
    request: Request,
    response: Response,
    cache: client.Redis = Depends(deps.get_redis),
) -> APIResponseType[schemas.Msg]:
    """Logout from system"""

    await services.logout(
        refresh_token=request.cookies.get("Refresh-Token"),
        access_token=request.cookies.get("Access-Token"),
        cache=cache,
    )
    response.delete_cookie(
        key="Refresh-Token",
        secure=True,
        httponly=True,
        samesite="strict" if not settings.DEBUG else "none",
    )
    response.delete_cookie(
        key="Access-Token",
        secure=True,
        httponly=True,
        samesite="strict" if not settings.DEBUG else "none",
    )
    return APIResponse(schemas.Msg(msg="You have successfully logged out"))
