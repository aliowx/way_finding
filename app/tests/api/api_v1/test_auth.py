import pytest
from httpx import AsyncClient, BasicAuth

from app.core.config import settings


@pytest.mark.asyncio
class TestAuth:
    email: str = "test@email.com"
    password: str = "test"

    @property
    def data(self):
        return {"email": TestAuth.email, "password": TestAuth.password}

    async def test_register(self, client: AsyncClient, superuser_tokens: dict):
        # normal register
        response = await client.post(
            f"{settings.API_V1_STR}/auth/register",
            json=self.data,
            cookies=superuser_tokens,
        )
        assert response.status_code == 200

        # duplicate register
        response = await client.post(
            f"{settings.API_V1_STR}/auth/register",
            json=self.data,
            cookies=superuser_tokens,
        )
        assert response.status_code == 409

    async def test_login(self, client: AsyncClient):

        # normal login
        response = await client.post(
            f"{settings.API_V1_STR}/auth/login", json=self.data
        )
        assert response.status_code == 200
        assert response.cookies.get("Access-Token") is not None
        assert response.cookies.get("Refresh-Token") is not None

        # invalid login
        response = await client.post(
            f"{settings.API_V1_STR}/auth/login",
            json={"invalied_username": "invalied_password"},
        )
        assert response.status_code == 400

    async def test_auth_and_tokens(self, client: AsyncClient):

        # normal login
        response = await client.post(
            f"{settings.API_V1_STR}/auth/login", json=self.data
        )
        assert response.status_code == 200

        cookies = dict(response.cookies.items())

        # call service with access and refresh tokens
        response = await client.get(f"{settings.API_V1_STR}/auth/me", cookies=cookies)
        assert response.status_code == 200
        assert TestAuth.email == response.json()["content"]["email"]

        # call service just with refresh token
        cookies.pop("Access-Token")
        response = await client.get(f"{settings.API_V1_STR}/auth/me", cookies=cookies)
        assert response.status_code == 200
        assert "" != client.cookies.get("Access-Token")
        assert None != client.cookies.get("Access-Token")

        # call service without tokens
        response = await client.get(f"{settings.API_V1_STR}/auth/me")
        assert response.status_code == 401

    async def test_basic_auth(self, client: AsyncClient):

        # call service with valid credential
        response = await client.get(
            f"{settings.API_V1_STR}/auth/me",
            auth=BasicAuth(settings.FIRST_SUPERUSER, settings.FIRST_SUPERUSER_PASSWORD),
        )
        assert response.status_code == 200
        assert settings.FIRST_SUPERUSER == response.json()["content"]["email"]

        # call service invalid credential
        response = await client.get(
            f"{settings.API_V1_STR}/auth/me", auth=BasicAuth("random", "random")
        )
        assert response.status_code == 401

        # call service without credential
        response = await client.get(f"{settings.API_V1_STR}/auth/me")
        assert response.status_code == 401
