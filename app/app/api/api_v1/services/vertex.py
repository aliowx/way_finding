import time 

from app import schemas, utils
from sqlalchemy.ext.asyncio import AsyncSession
from app import exceptions as exc
from app import crud 

async def register(db: AsyncSession, x_in: schemas.VertexCreate) -> schemas.Vertex:
    x = await crud.user.get_by_x(db=db, email=x_in.email)
    if x:
        raise exc.AlreadyExistException(
            detail="The user with this username already exists",
            msg_code=utils.MessageCodes.bad_request,
        )
    x = await crud.user.create(db=db, obj_in=x_in)
    return x