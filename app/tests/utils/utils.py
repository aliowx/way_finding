import random
import string
from typing import Dict

from httpx import AsyncClient

from app.core.config import settings


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


async def get_superuser_token_headers(client: AsyncClient) -> Dict[str, str]:
    payload = {
        "email": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    response = await client.post(f"{settings.API_V1_STR}/users/token", json=payload)
    tokens = response.json()
    access_token = tokens.get("access_token", None)
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers
