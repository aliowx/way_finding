from sqlalchemy import Column, Integer, Text, String

from app.db.base_class import Base


class WSRequestLog(Base):
    id = Column(Integer, primary_key=True, index=True)
    authorization = Column(String(256), nullable=True, index=True)
    method = Column(String(10), nullable=True, index=True)
    status_code = Column(String(10), nullable=True, index=True)
    service_name = Column(String(100), nullable=True, index=True)
    request = Column(Text, nullable=True, index=True)
    response = Column(Text, nullable=True)

    def __str__(self):
        return "%s:, %s" % (self.service_name, self.created)
