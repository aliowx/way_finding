from app.schemas.vertex import VertexCreate
import pytest
from httpx import AsyncClient, BasicAuth
from app.main import app
from app.core.config import settings
from fastapi import status
from fastapi.testclient import TestClient

@pytest.mark.asyncio
class TestVertex:
    endx: float = 100.5,
    endy: float = 200.5,
    startx: float = 10.5,
    starty: float = 20.5,
    pox: float = 1.0,
    poy: float = 2.0  
    
    @property
    def data(self):
        return {
        'endx': TestVertex.endx,
        'endy': TestVertex.endy,
        'startx': TestVertex.startx,
        'starty': TestVertex.starty,
        'pox': TestVertex.pox,
        'poy': TestVertex.poy       
    }

     
    async def test_register_input(
        self,
        client: AsyncClient
    )-> None:
        # normal input
        
        response = await client.post(
            f"{settings.API_V1_STR}/",
            json=self.data
        )   
        assert response.status_code == 200
    
    # duplicate input
    
        response = await client.post(
            f"{settings.API_V1_STR}/",
            json=self.data
        )
        assert response.status_code == 409


    async def test_multiple_requstes(
        self,
        client: AsyncClient
    )-> None:
        for i in range(10):
            response = await client.post(
                f'{settings.API_V1_STR}/',
                json=self.data
            )    
        try:
            assert response.status_code == 200
        except:                
            assert response.status_code == 404

    async def test_missing_data(
        self,
        client: AsyncClient
    )-> None:
        response = await client.get(f'{settings.API_V1_STR}/')
        assert response.status_code == 400
