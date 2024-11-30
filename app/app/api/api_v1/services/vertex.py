
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas, utils
from app import exceptions as exc
from app import crud 

async def create_vertex(
    db: AsyncSession,
    input: schemas.VertexCreate
    
)-> schemas.VertexCreate:
    
    vertex = await crud.vertex.get_(
        db=db,
        endx=input.endx,
        endy=input.endy,
        startx=input.startx,
        starty=input.starty,
        pox=input.pox,
        poy=input.poy
    )
    if vertex:
        raise exc.AlreadyExistException(
            detail="this position is already exist ",
            msg_code=utils.MessageCodes.bad_request,
        )
        
    return await crud.vertex.create(db=db, obj_in=input)
