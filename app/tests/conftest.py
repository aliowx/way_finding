import asyncio
import time
from typing import Generator, AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from httpx import AsyncClient

from app.api.deps import get_db_async
from app.app.schemas.vertex import VertexCreate
from app.main import app, settings
from app.db import Base
from app.crud import crud_user
from app.crud import crud_vertex
from app.core.security import JWTHandler
from app.db.init_db import init_db
from app.db import session as db_session


ASYNC_SQLALCHEMY_DATABASE_URL = f"sqlite+aiosqlite:///./test.db"

async_engine = create_async_engine(ASYNC_SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def override_get_db_async() -> AsyncGenerator:
    async with async_session() as db:
        yield db
        await db.commit()


app.dependency_overrides[get_db_async] = override_get_db_async


@pytest.fixture(autouse=True)
def patch_async_session_maker(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(db_session, "async_session", async_session)


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:  # noqa: indirect usage
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def db() -> AsyncSession: # type: ignore

    async with async_session() as session:
        async with async_engine.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)
            await connection.run_sync(Base.metadata.create_all)
        await init_db(db=session)
        yield session

    await async_engine.dispose()



@pytest_asyncio.fixture(scope="module")
async def client() -> AsyncClient: # type: ignore
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture(scope="session")
async def superuser_tokens(db: AsyncSession) -> dict[str, str]:  # noqa: indirect usage
    user = await crud_user.user.get_by_email(db=db, email=settings.FIRST_SUPERUSER)
    assert user != None

    refresh_token = JWTHandler.encode_refresh_token(
        payload={"sub": "refresh", "id": str(user.id)}
    )
    access_token = JWTHandler.encode(payload={"sub": "access", "id": str(user.id)})

    tokens = {"Refresh-Token": refresh_token, "Access-Token": access_token}
    return tokens


@pytest_asyncio.fixture(scope='session')
async def create_vertex(
    db: AsyncSession,
    superuser_tokens
):
    vertex_data = [
        VertexCreate(
            endx=10.5,
            endy=11.5,
            startx=12.5,
            starty=13.5,
            pox=14.5,
            poy=15.5  
        )
    ]
    
    if superuser_tokens is not None:

        new_vertex = await crud_vertex.vertex.create_multi(db=db, objs_in=vertex_data)
        db.add(new_vertex)

        await db.commit()
        
        yield new_vertex
        
        for vertex in new_vertex:
            await db.delete(vertex)
        
        await db.commit()