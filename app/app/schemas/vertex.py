from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True


class VertexCreate(BaseModel):
    x: float | None = None


class VertexUpdate(BaseModel):
    pass
