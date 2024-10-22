
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas, utils
from app import schemas, utils
from app import exceptions as exc
from app import crud 


async def register_position(
        db:AsyncSession,
        input:schemas.VertexCreate
):
    x = await crud.vertex.get_(
        db=db,
        endx=input.endx,
        endy=input.endy,
        startx=input.startx,
        starty=input.starty,
        pox=input.pox,
        poy=input.poy
    )


    if x:
        raise exc.AlreadyExistException(
            detail="this position is already exist ",
            msg_code=utils.MessageCodes.bad_request,
        )
    
    x = await crud.vertex.create(db=db,obj_in=input)
    return x 