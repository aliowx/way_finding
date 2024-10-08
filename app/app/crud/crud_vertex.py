from typing import Any

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.db.base_class import Base
from app.models.vertex import Vertex
from app.schemas.vertex import VertexCreate, VertexUpdate



class CRUDUser(CRUDBase[Vertex, VertexCreate, VertexUpdate]):
    pass