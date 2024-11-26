from sqlalchemy import Boolean, ForeignKey, Integer, String, Float
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.db.base_class import Base


class Edge(Base):
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    source_vertex_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vertex.id"), nullable=False
    )
    destination_vertex_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vertex.id"), nullable=False
    )

    distance: Mapped[float] = mapped_column(Float, nullable=True)

    source_vertex: Mapped["Vertex"] = relationship(
        "Vertex", foreign_keys=[source_vertex_id], back_populates="source_edges"
    )
    destination_vertex: Mapped["Vertex"] = relationship(
        "Vertex",
        foreign_keys=[destination_vertex_id],
        back_populates="destination_edges",
    )
