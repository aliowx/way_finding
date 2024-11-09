import pytest
from httpx import AsyncClient, BasicAuth
from app.main import app
from app import schemas, crud

from app.tests.conftest import create_vertex

@pytest.mark.asyncio
class TestVertexAPI:

    async def test_create_vertex(self, client: AsyncClient, create_vertex):

        new_vertex = create_vertex
        
        vertex_data = {
            "endx": new_vertex[0].endx,
            "endy": new_vertex[0].endy,
            "startx": new_vertex[0].startx,
            "starty": new_vertex[0].starty,
            "pox": new_vertex[0].pox,
            "poy": new_vertex[0].poy,
        }

        response = await client.post("/vertices/", json=vertex_data)

        assert response.status_code == 201


    async def test_get_vertex(self, client: AsyncClient, create_vertex):
        
        new_vertex = create_vertex
        vertex_id = new_vertex[0].id
    
        response = await client.get(f'/vertices/{vertex_id}/')
        
        assert response.status_code == 200
     
    
    async def tets_del_vertex(self, client: AsyncClient, create_vertex):
        pass
    