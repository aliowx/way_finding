from pydantic import BaseModel, ConfigDict
from typing import Optional

class VertexBase(BaseModel):
    x: float
    y: float
    name: str | None = False


class VertexCreate(VertexBase):
    x: float
    y: float

class VertexUpdate(VertexBase):
    x: float
    y: float


class VertexInDBBase(VertexBase):
    id: int | None = None
    model_config = ConfigDict(from_attributes=True)

# Additional properties to return via API
class User(VertexInDBBase):
    pass

