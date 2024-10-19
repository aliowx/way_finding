from sqlalchemy import Boolean, Integer, String, Float
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.db.base_class import Base


class Vertex(Base):
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    endx: Mapped[int] = mapped_column(Float, nullable=True)
    endy: Mapped[int] = mapped_column(Float, nullable=True)
    startx: Mapped[int] = mapped_column(Float, nullable=True)
    starty: Mapped[int] = mapped_column(Float, nullable=True)
    pox: Mapped[int] = mapped_column(Float, nullable=True)
    poy: Mapped[int] = mapped_column(Float, nullable=True)

    source_edges: Mapped[list["Edge"]] = relationship(
        "Edge", foreign_keys="[Edge.source_vertex_id]", back_populates="source_vertex"
    )
    destination_edges: Mapped[list["Edge"]] = relationship(
        "Edge",
        foreign_keys="[Edge.destination_vertex_id]",
        back_populates="destination_vertex",
    )
