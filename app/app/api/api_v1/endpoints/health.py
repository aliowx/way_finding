import secrets
from fastapi import APIRouter, Depends
from app.core.config import settings
from app import exceptions as exc
from app import utils
from app.api.deps import health_user

router = APIRouter()


@router.get("/ping", response_model=bool)
def ping(_=Depends(health_user)) -> bool:
    """
    return `true`
    """
    return True
