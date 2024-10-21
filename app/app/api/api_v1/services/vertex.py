
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas, utils
from app import schemas, utils
from app import exceptions as exc
from app import crud 

class VertexService:
    def __init__(self,db:AsyncSession):
        self.db = db  
    async def register_position(
            self,
            endx: schemas.VertexCreate,
            endy: schemas.VertexCreate,
            startx: schemas.VertexCreate,
            starty: schemas.VertexCreate,
            pox: schemas.VertexCreate,
            poy: schemas.VertexCreate,
    )-> schemas.vertex:
        x = await  crud.vertex.get_(
            db=self.db,
            endx=float,
            endy=float,
            startx=float,
            starty=float,
            pox=float,
            poy=float
        )

        if x:
            raise exc.AlreadyExistException(
                detail="this position is already exist ",
                msg_code=utils.MessageCodes.bad_request,
            )
        vertax_data = schemas.VertexCreate(

            endx=endx,
            endy=endy,
            startx=startx,
            starty=starty,
            pox=pox,
            poy=poy
        )
        x = await crud.vertex.create(db=self.db,obj_in=vertax_data)
        return x 