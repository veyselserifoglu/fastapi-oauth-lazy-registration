from contextlib import asynccontextmanager
import pytest

from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.services.dependencies import get_current_user
from app.models.sessions import Session as session_model
from app.core.database import get_db, Base

# setup a testing database engine 
# Use an in-memory SQLite database or a separate test database file
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test_sql_app.db"

# Create a new engine and sessionmaker for the test database
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables for the test database
Base.metadata.create_all(bind=engine)

# Override the `get_db` dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="module")
def test_db():
    app.dependency_overrides[get_db] = override_get_db
    yield
    # Optional cleanup: Drop all tables after the tests are done
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides[get_db] = None

# Automatically clean up sessions after each test
@pytest.fixture(autouse=True)
def cleanup_sessions():
    db = next(override_get_db())
    db.query(session_model).delete()
    db.commit()

# Custom dependency override function
def override_get_current_user():
    return {
        "username": "testuser",
        "user_session": {"session_token": "valid_session_token", "user_id": 1}
    }


"""
Solution was taken from: 
https://github.com/fastapi/fastapi/discussions/10833#discussioncomment-7945189
"""

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("starting up")
    yield
    print("shutting down")

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def async_client():
    async with lifespan(app):  # lifespan does not return the asgi app

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://localhost") as client:
            yield client

        # Cleanup after each test
        app.dependency_overrides.clear()

@pytest.fixture
def logged_in_client(async_client):
    # Apply the override only for this test
    app.dependency_overrides[get_current_user] = override_get_current_user
    yield async_client

@pytest.fixture
def logged_out_client(async_client):
    # Apply the override only for this test
    yield async_client