from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True


class VertexCreate(BaseModel):
    x: Optional[float] | None = None
    y: Optional[float] | None = None


class VertexUpdate(BaseModel):
    x: Optional[float] | None = None
    y: Optional[float] | None = None
    # name: Optional[bool] = None

    class Config:
        orm_mode = True


class VertexDelete(BaseModel):
    id: Optional[int] | None = None
    class Config:
        orm_mode = True
