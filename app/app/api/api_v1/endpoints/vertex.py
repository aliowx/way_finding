from fastapi import APIRouter, HTTPException, Depends 
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, models, schemas
from app.api import deps
from sqlalchemy import select
from app import exceptions as exc
from sqlalchemy import select
from app import exceptions as exc
from app import schemas
from app.api.api_v1.services.vertex import VertexService 
router = APIRouter()
namespace = "Position"



@router.post("/create_vertex/")
async def create_vertex(
    vertex_in: schemas.VertexCreate,

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
