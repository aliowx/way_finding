from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
import pytest

from app import crud
from app.core.config import settings
from app.schemas.user import UserCreate
from tests.utils.utils import random_email, random_lower_string


@pytest.mark.asyncio
async def test_get_users_superuser_me(
    client: AsyncClient, superuser_token_headers: Dict[str, str]
) -> None:
    response = await client.get(
        f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers
    )
    current_user = response.json().get("content")
    assert current_user
    assert response.status_code == 200
    assert current_user.get("is_active", None) is True
    assert current_user.get("is_superuser", None)
    assert current_user.get("email", None) == settings.FIRST_SUPERUSER


@pytest.mark.asyncio
async def test_get_users_normal_user_me(
    client: AsyncClient, normal_user_token_headers: Dict[str, str]
) -> None:
    response = await client.get(
        f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers
    )
    current_user = response.json().get("content")
    assert response.status_code == 200
    assert current_user.get("is_active", None) is True
    assert current_user.get("is_superuser", None) is False
    assert current_user.get("email", None) == settings.EMAIL_TEST_USER


@pytest.mark.asyncio
async def test_create_user_new_email(
    client: AsyncClient, superuser_token_headers: dict, db: AsyncSession
) -> None:
    email = random_email()
    password = random_lower_string()
    payload = {"email": email, "password": password}
    response = await client.post(
        f"{settings.API_V1_STR}/users/",
        headers=superuser_token_headers,
        json=payload,
    )
    assert 200 <= response.status_code < 300
    created_user = response.json().get("content")
    user = await crud.user.get_by_email(db, email=email)
    assert user
    assert user.email == created_user["email"]


@pytest.mark.asyncio
async def test_get_existing_user(
    client: AsyncClient, superuser_token_headers: dict, db: AsyncSession
) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = await crud.user.create(db, obj_in=user_in)
    user_id = user.id

    response = await client.get(
        f"{settings.API_V1_STR}/users/{user_id}",
        headers=superuser_token_headers,
    )
    assert 200 <= response.status_code < 300
    api_user = response.json().get("content")
    existing_user = await crud.user.get_by_email(db, email=email)
    assert existing_user
    assert existing_user.email == api_user["email"]


@pytest.mark.asyncio
async def test_create_user_existing_username(
    client: AsyncClient, superuser_token_headers: dict, db: AsyncSession
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    await crud.user.create(db, obj_in=user_in)
    payload = {"email": username, "password": password}
    response = await client.post(
        f"{settings.API_V1_STR}/users/",
        headers=superuser_token_headers,
        json=payload,
    )
    created_user = response.json().get("content")
    assert response.status_code == 400
    assert "_id" not in created_user


@pytest.mark.asyncio
async def test_create_user_without_login(client: AsyncClient) -> None:
    username = random_email()
    password = random_lower_string()
    payload = {"email": username, "password": password}
    response = await client.post(
        f"{settings.API_V1_STR}/users/",
        json=payload,
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_retrieve_users(
    client: AsyncClient, superuser_token_headers: dict, db: AsyncSession
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    await crud.user.create(db, obj_in=user_in)

    username2 = random_email()
    password2 = random_lower_string()
    user_in2 = UserCreate(email=username2, password=password2)
    await crud.user.create(db, obj_in=user_in2)

    response = await client.get(
        f"{settings.API_V1_STR}/users/", headers=superuser_token_headers
    )
    all_users = response.json().get("content")

    assert len(all_users) > 1
    for item in all_users:
        assert "email" in item
