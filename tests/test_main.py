import pytest

from fastapi import status
from httpx import AsyncClient
from httpx import ASGITransport

from app.main import app


@pytest.mark.asyncio
async def test_read_root():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")

    assert response.status_code == status.HTTP_200_OK
