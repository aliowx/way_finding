from pydantic import BaseModel


class EdgeBase(BaseModel):
    source_vertex_id: int
    destination_vertex_id: int
    distance: float


class EdgeCreate(EdgeBase):
    pass


class EdgeUpdate(EdgeBase):
    source_vertex_id: int | None = None
    destination_vertex_id: int | None = None
    distance: float | None = None
