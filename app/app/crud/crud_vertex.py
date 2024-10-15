from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.db.base_class import Base
from app.schemas.vertex import VertexCreate, VertexUpdate
from app.models.vertex import Vertex


class CRUDVertex(CRUDBase[Vertex, VertexCreate, VertexUpdate]):
    async def get_(self, db: AsyncSession, x: float, y: float) -> Vertex | None:
        query = select(self.model).where(
            and_(
                self.model.x == x,
                self.model.y == y,
                self.model.is_deleted.is_(True),
            )
        )
        response = await db.execute(query)
        return response.scalar_one_or_none()

    async def create_(db: AsyncSession, vertex: VertexCreate | dict) -> Base | Any:
        if isinstance:
            pass

    async def uodata_() -> None:
        pass

    async def del_() -> None:
        pass


vertex = CRUDVertex(Vertex)
