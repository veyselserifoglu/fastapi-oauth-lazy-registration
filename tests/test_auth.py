import pytest

from httpx import AsyncClient
from sqlalchemy.orm import Session
from fastapi import status


@pytest.mark.anyio
async def test_signup(async_client: AsyncClient) -> None:
    # Test data
    signup_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password123"
    }
    
    # Send a POST request to the signup endpoint
    response = await async_client.post("/auth/signup", data=signup_data)
    
    # Ensure the response is a redirect to the news page
    assert response.status_code == status.HTTP_303_SEE_OTHER
    assert response.headers["location"] == "/news/news"

@pytest.mark.anyio
async def test_logout(logged_in_client: AsyncClient):
    # Perform the logout
    response = await logged_in_client.get("/auth/logout")
    
    # Ensure the response is a redirect to the homepage
    assert response.status_code == 303
    assert response.headers["location"] == "/"
    
    # Check that the session token has been removed from cookies
    assert "session_token" not in response.cookies