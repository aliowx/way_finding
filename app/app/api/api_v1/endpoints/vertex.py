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
@cache(namespace = namespace, expire=ONE_DAY_IN_SECONDS)
async def read_users(
    db: AsyncSession = Depends(deps.get_db_async),
    position: float |None = None



):
    users = await crud.vertex.get_multi(db)
    print(users)
    return users

@router.post("/")
@cache(namespace = namespace, expire=ONE_DAY_IN_SECONDS)
async def create_vertax(
    db: AsyncSession = Depends(deps.get_db_async),
    *,
    vertex_in: schemas.VertexCreate,
):
    x = await crud.vertex.create(db, obj_in = vertex_in)
    return x

@router.delete('/{id}')
@cache(namespace = namespace, expire=ONE_DAY_IN_SECONDS)
async def delet_vertax(
    db:AsyncSession =Depends(deps.get_db_async),
    *,
    id:int
):
    x_= await crud.vertex.remove(db, id_ = id)
    return x_