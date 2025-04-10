
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, models, schemas
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
            db=db,input=vertex_in
        )
    except Exception as e:
        raise e
    return new_vertex


router = APIRouter()
namespace = "Position"



@router.post("/create_vertex/")
async def create_vertex(
    vertex_in: schemas.VertexCreate,

    db: AsyncSession = Depends(deps.get_db_async),
    *,
    vertex_in: schemas.VertexCreate,
):

    result = await db.execute(
        select(crud.vertex.model).filter_by(x=vertex_in.x, y=vertex_in.y)
    )
    existing_vertex = result.scalars().first()
    if existing_vertex:
        raise exc.AlreadyExistException(
            detail="The position already exists!",
            msg_code=utils.MessageCodes.bad_request,
        )
    existing_vertex = await crud.vertex.create(db, obj_in=vertex_in)
    return existing_vertex
    

@router.get("/")
@cache(namespace=namespace, expire=ONE_DAY_IN_SECONDS)
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
