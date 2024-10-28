from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, models, schemas
from app.api import deps
from app import schemas
from app.api.api_v1.services import vertex


router = APIRouter()
namespace = "Position"


@router.post("/")
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


@router.get("/")
async def read_users(
    vertex_in: schemas.VertexCreate,
    db:AsyncSession = Depends(deps.get_db_async),
    current_user : models.User = Depends(
        deps.get_current_superuser_from_cookie_or_basic
    )
):
    return vertex_in


@router.delete("/{id}")
async def delet_vertax(
    db: AsyncSession = Depends(deps.get_db_async),
    current_user : models.User = Depends(
        deps.get_current_superuser_from_cookie_or_basic
    ),
):
    x_ = await crud.vertex.remove(db, id_=id)
    return x_
