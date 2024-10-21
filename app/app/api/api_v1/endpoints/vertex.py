from fastapi import APIRouter, HTTPException, Depends 
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas
from app.api import deps
from sqlalchemy import select
from app import exceptions as exc
from app import schemas
from app.api.api_v1.services.vertex import VertexService 
router = APIRouter()
namespace = "Position"


@router.post("/")
async def create_vertax(
    db: AsyncSession = Depends(deps.get_db_async),
    *,
    vertex_in: schemas.VertexCreate,
):
    vertx_servis = VertexService(db)

    try:
        new_vertex = await vertx_servis.register_position(
            endx=vertex_in.endx,
            endy=vertex_in.endy,
            startx=vertex_in.startx,
            starty=vertex_in.starty,
            pox=vertex_in.pox,
            poy=vertex_in.poy,
        )
        return new_vertex
    except HTTPException as e:
        raise e




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
