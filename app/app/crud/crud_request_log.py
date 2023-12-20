from app.crud.base import CRUDBase
from app.models.request_log import RequestLog
from app.schemas.request_log import RequestLogCreate, RequestLogUpdate


class CRUDRequestLog(CRUDBase[RequestLog, RequestLogCreate, RequestLogUpdate]):
    pass


request_log = CRUDRequestLog(RequestLog)
