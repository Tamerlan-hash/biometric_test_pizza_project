import json
import os
import pytest
import pytest_asyncio

from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from settings.database import async_engine
from settings.database.connection import Base

from main import app


@pytest_asyncio.fixture
async def async_client(test_app: FastAPI = app) -> AsyncClient:
    async with LifespanManager(test_app):
        async with AsyncClient(
            app=test_app,
            base_url="http://localhost:8000",
            headers={"Content-Type": "application/json"}
        ) as client:
            yield client


@pytest_asyncio.fixture(scope="function")
async def async_session():
    async_session_maker = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session_maker() as session:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield session

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await async_engine.dispose()


@pytest.fixture(scope="function")
def test_restaurant_data() -> dict:
    path = os.getenv('PYTEST_CURRENT_TEST')
    path = os.path.join(*os.path.split(path)[:-1], "data", "restaurant.json")

    if not os.path.exists(path):
        path = os.path.join("data", "restaurant.json")

    with open(path, "r") as file:
        data = json.loads(file.read())

    return data


@pytest.fixture(scope="function")
def test_pizza_data() -> dict:
    path = os.getenv('PYTEST_CURRENT_TEST')
    path = os.path.join(*os.path.split(path)[:-1], "data", "pizza.json")

    if not os.path.exists(path):
        path = os.path.join("data", "pizza.json")

    with open(path, "r") as file:
        data = json.loads(file.read())

    return data
