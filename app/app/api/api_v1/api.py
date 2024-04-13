from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, users, utils, health

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(utils.router_with_log, prefix="/utils", tags=["utils"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
