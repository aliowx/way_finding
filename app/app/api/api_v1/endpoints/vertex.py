from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app import crud,schemas

from app.api import deps
from cache import cache
from cache.util import ONE_DAY_IN_SECONDS


router = APIRouter()
namespace = "vertex"

@router.get("/")
@cache(namespace=namespace, expire=ONE_DAY_IN_SECONDS)
async def read_users(
    db: AsyncSession = Depends(deps.get_db_async),
    position: float = 0
) -> List[schemas.User]:
    users = await crud.vertex.get_multi(db, position=position)
    return [schemas.User.model_config(user) for user in users]

@router.post("/")
@cache(namespace=namespace, expire=ONE_DAY_IN_SECONDS)
async def create_vertax(
    db: AsyncSession = Depends(deps.get_db_async),
    *,
    vertex_in: schemas.VertexCreate,
):
    users = await crud.vertex.create(db, obj_in = vertex_in)
    return users