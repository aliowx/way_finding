<<<<<<< HEAD
from fastapi import APIRouter, HTTPException, Depends 
=======
from fastapi import APIRouter, Depends, HTTPException
>>>>>>> origin/feature/add-test
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, models, schemas
from app.api import deps
<<<<<<< HEAD
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
            db=db,input=vertex_in
        )
    except Exception as e:
        raise e
    return new_vertex


@router.get("/")
async def read_users(
=======
from app import schemas
from app.api.api_v1.services import vertex
from app.utils import APIResponse, APIResponseType


router = APIRouter()
namespace = "Position"


@router.post("/create_vertex/")
async def create_vertex(
    vertex_in: schemas.VertexCreate,
>>>>>>> origin/feature/add-test
    db: AsyncSession = Depends(deps.get_db_async),
    _: models.User = Depends(deps.get_current_superuser_from_cookie_or_basic)
       
)-> APIResponseType[schemas.Vertex]:
    
    response = await vertex.create_vertex(db=db, input=vertex_in)
    
    return APIResponse[response]


<<<<<<< HEAD

=======
@router.get("/vertices/{vertex_id}/", response_model=schemas.Vertex)
async def read_vertex(
    vertex_id: int,
    db: AsyncSession = Depends(deps.get_db_async),
    _: models.User = Depends(deps.get_current_superuser_from_cookie_or_basic)
    
)-> APIResponseType[list[schemas.Vertex]]:

    response = await crud.vertex.get_by_id(db=db, vertex_id=vertex_id)

    if not vertex:
        raise HTTPException(status_code=404, detail="Vertex not found")

    return response

@router.delete("/{id}")
async def delete_vertex(
    db: AsyncSession = Depends(deps.get_db_async),
    current_user : models.User = Depends(deps.get_current_superuser_from_cookie_or_basic),
):
    response = await crud.vertex.remove(db, id_=id)
    return response
>>>>>>> origin/feature/add-test
