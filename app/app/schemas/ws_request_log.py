from typing import Optional

from pydantic import BaseModel


class WSRequestLogCreate(BaseModel):
    authorization: str = None
    request: str = None
    response: str = None
    service_name: str = None
    method: str = None
    status_code: Optional[str] = None


class WSRequestLogUpdate(BaseModel):
    pass
