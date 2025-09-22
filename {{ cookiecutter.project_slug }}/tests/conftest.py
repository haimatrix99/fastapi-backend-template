import asyncio

import pytest
from app.infrastructure.database import Base, get_db
from fastapi.testclient import TestClient
from main import app
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Use an in-memory SQLite database for tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create test engine (use StaticPool so the in-memory DB persists across connections)
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    poolclass=StaticPool,
)

# Create test session factory
TestSessionLocal = sessionmaker(
    bind=test_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(scope="session")
def test_db():
    """Create a test database and initialize tables (sync wrapper)."""

    async def _init():
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(_init())
    yield

    async def _teardown():
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await test_engine.dispose()

    asyncio.run(_teardown())


@pytest.fixture(scope="function")
def client(test_db):
    """Create a test client with a database session override and clean DB per test."""

    # Reset DB state before each test to ensure isolation
    async def _reset():
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(_reset())

    async def override_get_db():
        async with TestSessionLocal() as session:
            try:
                yield session
            finally:
                await session.rollback()

    # Override the get_db dependency to use the test session
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    # Clean up
    app.dependency_overrides.clear()
