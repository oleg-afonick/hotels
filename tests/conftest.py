import json
import pytest
from httpx import AsyncClient

from src.schemas.comforts import ComfortSchemaPostPut
from src.schemas.hotels import HotelSchemaPostPut
from src.schemas.rooms import RoomSchemaPostPut
from src.database import engine_null_pool, Base
from src.config import settings
from src.models import *
from src.main import app
from src.api.dependencies import db_session
from src.database import async_session_maker_null_pool


@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="function")
async def db(setup_database) -> db_session:
    async with db_session(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="session")
async def ac(setup_database) -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def test_user_register(ac, setup_database):
    await ac.post("/auth/register", json={"email": "test@test.ru", "password": "test"})


@pytest.fixture(scope="session", autouse=True)
async def test_add_objects(setup_database):
    with open("tests/mocks/mock_hotels.json", encoding="utf-8") as file_hotels:
        hotels_json = json.load(file_hotels)
    with open("tests/mocks/mock_rooms.json", encoding="utf-8") as file_rooms:
        rooms_json = json.load(file_rooms)
    async with db_session(session_factory=async_session_maker_null_pool) as session_db:
        hotels_data = [HotelSchemaPostPut.model_validate(hotel) for hotel in hotels_json]
        rooms_data = [RoomSchemaPostPut.model_validate(room) for room in rooms_json]
        await  session_db.hotels.add_multiple(hotels_data)
        await  session_db.rooms.add_multiple(rooms_data)
        await session_db.commit()

