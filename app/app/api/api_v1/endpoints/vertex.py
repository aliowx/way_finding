from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas
from app.api import deps
from cache import cache
from cache.util import ONE_DAY_IN_SECONDS
from sqlalchemy import select
from app import exceptions as exc
from app import schemas, utils
import pandas as pd 


router = APIRouter()
namespace = "Position"

df = pd.read_csv(r'/home/ali/Desktop/data1.csv')


@router.post("/")
@cache(namespace=namespace, expire=ONE_DAY_IN_SECONDS)
async def create_vertax(
    db: AsyncSession = Depends(deps.get_db_async),
    *,
    vertex_in: schemas.VertexCreate,df
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
    
    try:
        for index, row in df.iterrows():
            vertex_form_df = crud.vertex.model(
            x = row['start x'],
            y = row['start y']

            )
        db.add(vertex_form_df
        )
        await db.commit()

    except IndentationError:
        await db.rollback()
        raise exc.AlreadyExistException(
            detail = "some position in the csv already exist!",
            msg_code=utils.MessageCodes.bad_request,
        )
    return {"msg": "Vertices created successfully from CSV."}


@router.get("/")
@cache(namespace=namespace, expire=ONE_DAY_IN_SECONDS)
async def read_users(
    db: AsyncSession = Depends(deps.get_db_async),
    X: float | None = None,
    Y: float | None = None,
):
    position = await crud.vertex.get_multi(db)
    return position


@router.delete("/{id}")
@cache(namespace=namespace, expire=ONE_DAY_IN_SECONDS)
async def delet_vertax(db: AsyncSession = Depends(deps.get_db_async), *, id: int):
    x_ = await crud.vertex.remove(db, id_=id)
    return x_
