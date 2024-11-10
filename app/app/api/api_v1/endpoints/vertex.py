from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, models, schemas
from app.api import deps
from app import schemas
from app.api.api_v1.services import vertex


router = APIRouter()
namespace = "Position"


@router.post("/create_vertex/")
async def create_vertex(
    vertex_in: schemas.VertexCreate,
    db: AsyncSession = Depends(deps.get_db_async),
    _: models.User = Depends(
        deps.get_current_superuser_from_cookie_or_basic
    ),
):
    try:
        new_vertex = await vertex.register_position(db=db, input=vertex_in)
    except Exception as e:
        raise e
    return new_vertex


@router.get("/vertices/{vertex_id}/", response_model=schemas.Vertex)
async def read_vertex(
    vertex_id: int,
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_superuser_from_cookie_or_basic)
):

    vertex = await crud.vertex.get_by_id(db=db, vertex_id=vertex_id)

    if not vertex:
        raise HTTPException(status_code=404, detail="Vertex not found")

    return vertex


@router.delete("/{id}")
async def delete_vertex(
    db: AsyncSession = Depends(deps.get_db_async),
    current_user : models.User = Depends(
        deps.get_current_superuser_from_cookie_or_basic
    ),
):
    x_ = await crud.vertex.remove(db, id_=id)
    return x_
