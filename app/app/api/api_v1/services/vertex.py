
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas, utils
from app import exceptions as exc
from app import crud 

<<<<<<< HEAD

async def register_position(
        db:AsyncSession,
        input:schemas.VertexCreate
):
    x = await crud.vertex.get_(
=======
async def create_vertex(
    db: AsyncSession,
    input: schemas.VertexCreate
    
)-> schemas.VertexCreate:
    
    vertex = await crud.vertex.get_(
>>>>>>> origin/feature/add-test
        db=db,
        endx=input.endx,
        endy=input.endy,
        startx=input.startx,
        starty=input.starty,
        pox=input.pox,
        poy=input.poy
    )
<<<<<<< HEAD


    if x:
=======
    if vertex:
>>>>>>> origin/feature/add-test
        raise exc.AlreadyExistException(
            detail="this position is already exist ",
            msg_code=utils.MessageCodes.bad_request,
        )
<<<<<<< HEAD
    
    x = await crud.vertex.create(db=db,obj_in=input)
    return x 
=======
        
    return await crud.vertex.create(db=db, obj_in=input)
>>>>>>> origin/feature/add-test
