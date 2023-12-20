from typing import Any, Dict

import pytest
from httpx import AsyncClient

from app.core.config import settings


@pytest.mark.asyncio
class TestAuth:
    email: str = "test@email.com"
    password: str = "test"
    headers: Dict[str, str] | None = None
    access_token: Any = None
    refresh_token: Any = None

    @property
    def data(self):
        return {"email": TestAuth.email, "password": TestAuth.password}

    async def test_register(self, client: AsyncClient):
        response = await client.post(f"{settings.API_V1_STR}/auth/register", json=self.data)
        assert response.status_code == 200
        response = await client.post(f"{settings.API_V1_STR}/auth/register", json=self.data)
        assert response.status_code == 400

    async def test_login(self, client: AsyncClient):
        response = await client.post(f"{settings.API_V1_STR}/auth/login", json=self.data)
        assert response.status_code == 200
        assert response.cookies.get("Access-Token") is None
        assert response.cookies.get("Refresh-Token") is not None
        TestAuth.refresh_token = response.cookies["Refresh-Token"]
        TestAuth.headers = {"Authorization": "Bearer " + TestAuth.refresh_token}
        corrupted_data = self.data.copy()
        corrupted_data["email"] = "test"
        response = await client.post(f"{settings.API_V1_STR}/auth/login", json=corrupted_data)
        assert response.status_code == 400

        client.cookies.update(
            {"Access-Token": TestAuth.access_token, "Refresh-Token": TestAuth.refresh_token}
        )

    async def test_refresh_token(self, client: AsyncClient):
        response = await client.post(f"{settings.API_V1_STR}/auth/refresh", headers=TestAuth.headers)
        assert response.status_code == 200
        new_access_token = response.cookies.get("Access-Token")
        new_refresh_token = response.cookies.get("Refresh-Token")
        assert new_access_token is not None
        assert new_refresh_token is not None
        assert new_access_token != TestAuth.access_token
        assert new_refresh_token != TestAuth.refresh_token
        TestAuth.refresh_token = new_refresh_token
        TestAuth.access_token = new_access_token
        headers = {"Authorization": "Bearer " + TestAuth.access_token}
        assert type(TestAuth.headers) is dict
        assert headers["Authorization"] != TestAuth.headers.get("Authorization")

        client.cookies.update(
            {"Access-Token": new_access_token, "Refresh-Token": new_refresh_token}
        )
        response = await client.get(f"{settings.API_V1_STR}/auth/me", headers=headers)
        assert response.status_code == 200
        TestAuth.headers = {"Authorization": "Bearer " + new_access_token}

    async def test_auth_and_tokens(self, client: AsyncClient):
        response = await client.get(f"{settings.API_V1_STR}/auth/me", headers=TestAuth.headers)
        assert response.status_code == 200
        assert TestAuth.email == response.json()["content"]["email"]

        bad_header = {"Authorization": "Bearer " + TestAuth.refresh_token}
        response = await client.get(f"{settings.API_V1_STR}/auth/me", headers=bad_header)
        assert response.status_code == 401

        bad_header = {"Authorization": TestAuth.access_token}
        response = await client.get(f"{settings.API_V1_STR}/auth/me", headers=bad_header)
        assert response.status_code == 403
