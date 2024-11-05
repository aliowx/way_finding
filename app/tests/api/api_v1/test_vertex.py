import pytest
from httpx import AsyncClient, BasicAuth
from app.core.config import settings
from app import schemas


@pytest.mark.asyncio
class TestVertexAPI:

    async def test_create_vertex(self, client: AsyncClient):
        vertex_data = {
            "name": "Vertex1",
            "endx": 10.5,
            "endy": 20.5,
            "startx": 30.5,
            "starty": 40.5,
            "pox": 50.5,
            "poy": 60.5
        }
        response = await client.post(
            f"{settings.API_V1_STR}/vertices/",
            json=vertex_data,
            auth=BasicAuth(
                username=settings.HEALTH_USERNAME, password=settings.HEALTH_PASSWORD
            ),
        )
        assert response.status_code == 201  
        assert "id" in response.json()  
        self.created_vertex_id = response.json()["id"]  

    async def test_read_vertex(self, client: AsyncClient):
        response = await client.get(
            f"{settings.API_V1_STR}/vertices/{self.created_vertex_id}",
            auth=BasicAuth(
                username=settings.HEALTH_USERNAME, password=settings.HEALTH_PASSWORD
            ),
        )
        assert response.status_code == 200 
        vertex_data = response.json()
        assert vertex_data["id"] == self.created_vertex_id  
        assert vertex_data["name"] == "Vertex1" 
        assert vertex_data["endx"] == 10.5  
        assert vertex_data["endy"] == 20.5
        assert vertex_data['startx'] == 30.5
        assert vertex_data['starty'] == 40.5
        assert vertex_data['pox'] == 50.5
        assert vertex_data['poy'] == 60.5

    async def test_delete_vertex(self, client: AsyncClient):
        response = await client.delete(
            f"{settings.API_V1_STR}/vertices/{self.created_vertex_id}",
            auth=BasicAuth(
                username=settings.HEALTH_USERNAME, password=settings.HEALTH_PASSWORD
            ),
        )
        assert response.status_code == 204  

        response = await client.get(
            f"{settings.API_V1_STR}/vertices/{self.created_vertex_id}",
            auth=BasicAuth(
                username=settings.HEALTH_USERNAME, password=settings.HEALTH_PASSWORD
            ),
        )
        assert response.status_code == 404  
