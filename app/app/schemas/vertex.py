from pydantic import BaseModel
from typing import Optional


class Vertex(BaseModel):
    endx: float
    endy: float
    startx: float
    starty: float
    pox: float
    poy: float
    
    class Config:
        from_attributes = True


class VertexCreate(BaseModel):
    endx: float
    endy: float
    startx: float
    starty: float
    pox: float
    poy: float
    

class VertexUpdate(BaseModel):
    endx: float
    endy: float
    startx: float
    starty: float
    pox: float
    poy: float

    class Config:
        from_attributes = True


class VertexDelete(BaseModel):
    id: Optional[int] | None = None
    class Config:
        from_attributes = True
