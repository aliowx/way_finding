from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select

from app.crud.base import CRUDBase
from app.models.edge import Edge
from app.schemas.edge import EdgeCreate, EdgeUpdate


class CRUDEdge(CRUDBase[Edge, EdgeCreate, EdgeUpdate]):
    pass


edge = CRUDEdge(Edge)
