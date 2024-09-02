import pytest

from httpx import AsyncClient
from httpx import ASGITransport
from fastapi import status

from app.main import app


@pytest.mark.anyio
async def test_show_news(async_client: AsyncClient) -> None:
    response = await async_client.get("/news/news")

    assert response.status_code == status.HTTP_200_OK
    
    assert "session_token" in response.cookies

@pytest.mark.anyio
async def test_add_comment_anonymous(logged_out_client: AsyncClient) -> None:
    response = await logged_out_client.get("/news/comment")

    assert response.status_code == status.HTTP_200_OK

    # Check if the title of the signup page is present
    assert "<title>Sign Up</title>" in response.text  

@pytest.mark.anyio
async def test_add_comment_logged_in(logged_in_client: AsyncClient) -> None:
    response = await logged_in_client.get("/news/comment")
    
    assert response.status_code == status.HTTP_200_OK

    # Check if the title of the news headline page is present
    assert "<title>News Headlines</title>" in response.text
