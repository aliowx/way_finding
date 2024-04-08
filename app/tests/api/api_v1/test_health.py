import pytest
from httpx import AsyncClient, BasicAuth

from app.core.config import settings


@pytest.mark.asyncio
class TestHealth:

    async def test_ping(self, client: AsyncClient):
        response = await client.get(
            f"{settings.API_V1_STR}/health/ping",
            auth=BasicAuth(
                username=settings.HEALTH_USERNAME, password=settings.HEALTH_PASSWORD
            ),
        )
        assert response.status_code == 200
        assert response.text == "true"
