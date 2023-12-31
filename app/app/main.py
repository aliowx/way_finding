from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware import Middleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.core.middleware import SessionMiddleware
from app.exceptions import exception_handlers
from app.models import User
from cache import Cache


def make_middleware() -> list[Middleware]:
    middleware = [Middleware(SessionMiddleware)]
    return middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_cache = Cache()
    url = str(settings.REDIS_URI)
    await redis_cache.init(
        host_url=url,
        prefix="api-cache",
        response_header="X-API-Cache",
        ignore_arg_types=[Request, Response, Session, AsyncSession, User],
    )
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
    exception_handlers=exception_handlers,
    middleware=make_middleware(),
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

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(api_router, prefix=settings.API_V1_STR)
