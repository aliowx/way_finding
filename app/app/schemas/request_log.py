from datetime import datetime

from pydantic import ConfigDict, BaseModel


class RequestLogInDBBase(BaseModel):
    id: int
    created: datetime
    modified: datetime
    model_config = ConfigDict(from_attributes=True)


class RequestLogCreate(BaseModel):
    request: str = None
    response: str = None
    service_name: str = None
    method: str = None
    authorization: str | None = None
    ip: str | None = None
    trace: str | None = None


class RequestLogUpdate(BaseModel):
    pass
