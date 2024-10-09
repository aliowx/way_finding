from pydantic import BaseModel


class VertexBase(BaseModel):
    x: float
    y: float
    name: str
    description: str


class VertexCreate(VertexBase):
    pass


class VertexUpdate(VertexBase):
    x: float | None = None
    y: float | None = None
    name: str | None = None
    description: str | None = None
