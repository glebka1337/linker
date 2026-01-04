import pytest_asyncio
from httpx import (
    AsyncClient,
    ASGITransport
)
from src.main import app

@pytest_asyncio.fixture
async def http_client(
    mongo_test_db
):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac