import json
import pytest
from httpx import AsyncClient

from src.database import engine_null_pool, Base
from src.config import settings
from src.models import *
from src.main import app


@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def test_user_register(setup_database):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/auth/register", json={"email": "test@test.ru", "password": "test"})


@pytest.fixture(scope="session", autouse=True)
async def test_add_hotels(setup_database):
    with open("tests/mock_hotels.json", encoding="utf-8") as file:
        hotels_data = json.load(file)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        for hotel in hotels_data:
            await ac.post("/hotels", json=hotel)

@pytest.fixture(scope="session", autouse=True)
async def test_add_comforts(test_add_hotels):
    with open("tests/mock_comforts.json", encoding="utf-8") as file:
        comforts_data = json.load(file)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        for comfort in comforts_data:
            await ac.post("/comforts", json=comfort)


@pytest.fixture(scope="session", autouse=True)
async def test_add_rooms(test_add_comforts):
    with open("tests/mock_rooms.json", encoding="utf-8") as file:
        rooms_data = json.load(file)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        for room in rooms_data:
            hotel_id = room.pop('hotel_id')
            await ac.post(f"/hotels/{hotel_id}/rooms/", json=room)
