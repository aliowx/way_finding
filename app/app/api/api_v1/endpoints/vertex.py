from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas
from app.api import deps
from sqlalchemy import select
from app import exceptions as exc
from app import schemas, utils


router = APIRouter()
namespace = "Position"


@router.post("/")
async def create_vertax(
    db: AsyncSession = Depends(deps.get_db_async),
    *,
    vertex_in: schemas.VertexCreate,
):

    existing_vertex = await crud.vertex.create(db, obj_in=vertex_in)
    return existing_vertex


@router.get("/")
async def read_users(
    db: AsyncSession = Depends(deps.get_db_async),
    X: float | None = None,
    Y: float | None = None,
):
    position = await crud.vertex.get_multi(db)
    return position


@router.delete("/{id}")
async def delet_vertax(db: AsyncSession = Depends(deps.get_db_async), *, id: int):
    x_ = await crud.vertex.remove(db, id_=id)
    return x_
