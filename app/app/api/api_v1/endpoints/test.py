from fastapi import APIRouter,HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas
from app.api import deps
from app import schemas
from app.api.api_v1.services import test


router = APIRouter(tags='test')

async def test_action(
        current_user=Depends(deps.get_current_superuser_from_cookie_or_basic),
        db: AsyncSession = Depends(deps.get_db_async)
)->None:
    pass