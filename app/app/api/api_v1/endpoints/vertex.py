from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps
from app.api.api_v1 import services
from app.log import log
from app.utils import APIResponse, APIResponseType
from cache import cache, invalidate
from cache.util import ONE_DAY_IN_SECONDS


router = APIRouter()
namespace = "vertex"

@router.get("/{position}")
@cache(namespace=namespace, expire=ONE_DAY_IN_SECONDS)
async def get_x(
    position: float,
    current_user: models.User = Depends(deps.get_current_superuser_from_cookie_or_basic),
    db: AsyncSession = Depends(deps.get_db_async),
) -> APIResponseType[schemas.User]:
    """
    Get a specific Position.
    """
    response = await services.read_user_by_id(
        db=db, position=position, current_user=current_user
    )
    return APIResponse(response)