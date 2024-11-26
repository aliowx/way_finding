from app.schemas.vertex import VertexCreate
import pytest
from httpx import AsyncClient, BasicAuth
from app.main import app
from app.core.config import settings
from fastapi import status
from fastapi.testclient import TestClient

@pytest.mark.asyncio
class TestVertex:

    async def test_create_vertex_post(client: AsyncClient):
        vertex_data = VertexCreate(
                endx = 100.5,
                endy = 200.5,
                startx = 10.5,
                starty = 20.5,
                pox = 1.0,
                poy = 2.0  
        )

        api_url = f"{settings.API_V1_STR}/create_vertex/"

        response = client.post(
            api_url,
            json=vertex_data.model_dump(),
            auth=BasicAuth(
                username=settings.HEALTH_USERNAME,
                password=settings.HEALTH_PASSWORD 
            )
        )

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        created_vertex_id = response_data.get('id')
        return created_vertex_id

    async def test_create_vertex_get(client:AsyncClient, vertex_id:int):
            
        api_url = f"{settings.API_V1_STR}vertices/{vertex_id}/"

        response = await client.get(
            api_url,
            auth=BasicAuth(
                username=settings.HEALTH_USERNAME,
                password=settings.HEALTH_PASSWORD 
            )
        )

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data == vertex_id

    async def test_create_vertex_del(client:AsyncClient,id:int):

        api_url = f"{settings.API_V1_STR}/{id}"

        response = await client.delete(
            api_url,
            auth=BasicAuth(
                username=settings.HEALTH_USERNAME,
                password=settings.HEALTH_PASSWORD 
            )
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND