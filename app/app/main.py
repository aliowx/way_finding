from fastapi import FastAPI, Request, Response
from starlette.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.models import User
from app.exceptions import exception_handlers
from cache import Cache

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    exception_handlers=exception_handlers,
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup():
    redis_cache = Cache()
    url = f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_SERVER}:{settings.REDIS_PORT}"
    await redis_cache.init(
        host_url=url,
        prefix="api-cache",
        response_header="X-API-Cache",
        ignore_arg_types=[Request, Response, Session, AsyncSession, User],
    )
