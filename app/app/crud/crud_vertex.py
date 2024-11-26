from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.db.base_class import Base
from app.schemas.vertex import VertexCreate, VertexUpdate
from app.models.vertex import Vertex
from typing import Any


class CRUDVertex(CRUDBase[Vertex, VertexCreate, VertexUpdate]):
    async def get_(
        self,
        db: AsyncSession,
        endx: float,
        endy: float,
        startx: float,
        starty: float,
        pox: float,
        poy: float,
    ) -> Vertex | None:

        query = select(self.model).where(
            and_(
                self.model.endx == endx,
                self.model.endy == endy,
                self.model.startx == startx,
                self.model.starty == starty,
                self.model.pox == pox,
                self.model.poy == poy,
                self.model.is_deleted.is_(None),
            )
        )
        
        response = await db.execute(query)
        return response.scalar_one_or_none()
    async def get_multi(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> list[Vertex]:
        query = select(self.model).offset(skip).limit(limit)
        response = await db.execute(query)  
        return response.scalars().all()  



vertex = CRUDVertex(Vertex)
