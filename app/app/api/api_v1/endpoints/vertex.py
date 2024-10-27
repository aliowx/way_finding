from fastapi import APIRouter, HTTPException, Depends 
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas
from app.api import deps
from sqlalchemy import select
from app import exceptions as exc
from app import schemas
from app.api.api_v1.services import vertex

router = APIRouter()
namespace = "Position"


@router.post("/")
async def create_vertax(
    db: AsyncSession = Depends(deps.get_db_async),
    *,
    vertex_in: schemas.VertexCreate,
):
    try:
        new_vertex = await vertex.register_position(
            db=db, input=vertex_in
        )
    except Exception as e:
        raise e
    return new_vertex


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
