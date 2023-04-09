from app.crud.base import CRUDBase
from app.schemas.ws_request_log import (WSRequestLogCreate, WSRequestLogUpdate)
from app.models.ws_request_log import WSRequestLog


class CRUDWSRequestLog(CRUDBase[WSRequestLog, WSRequestLogCreate, WSRequestLogUpdate]):
    pass


ws_request_log = CRUDWSRequestLog(WSRequestLog)
