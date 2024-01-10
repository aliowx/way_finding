from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import mapped_column

from app.db.base_class import Base


class RequestLog(Base):
    id = mapped_column(Integer, primary_key=True)

    authorization = mapped_column(String(256))
    method = mapped_column(String(10))
    service_name = mapped_column(String(50))
    ip = mapped_column(String(50))
    request = mapped_column(Text)
    response = mapped_column(Text)
    trace = mapped_column(Text, default="")

    def __str__(self):
        return "%s: %s, %s" % (self.service_name, self.ip, self.created)
