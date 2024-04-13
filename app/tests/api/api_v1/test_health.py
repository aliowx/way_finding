import pytest
from httpx import AsyncClient, BasicAuth

from app.core.config import settings
from app import schemas


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

    async def test_check(self, client: AsyncClient):
        response = await client.get(
            f"{settings.API_V1_STR}/health/check",
            auth=BasicAuth(
                username=settings.HEALTH_USERNAME, password=settings.HEALTH_PASSWORD
            ),
        )

        assert response.status_code == 200

        response_data = schemas.HealthCheck(**response.json())
        assert response_data.services.postgres.ok == True
        assert response_data.services.redis.ok == True
