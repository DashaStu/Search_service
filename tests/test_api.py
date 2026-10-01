import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_search():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/search", params={"query": "конкурс"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_delete():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete("/documents/1") 
    assert response.status_code == 204