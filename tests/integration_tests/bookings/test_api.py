import pytest

from src.api.dependencies import db_session
from src.database import async_session_maker


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1, "2025-01-05", "2025-01-10", 200),
    (1, "2025-01-06", "2025-01-11", 200),
    (1, "2025-01-07", "2025-01-12", 200),
    (1, "2025-01-08", "2025-01-13", 200),
    (1, "2025-01-09", "2025-01-14", 200),
    (1, "2025-01-10", "2025-01-15", 500),
    (1, "2025-01-17", "2025-01-27", 200)
])
async def test_add_bookings(room_id, date_from, date_to, status_code, db, auth_ac):
    room = await db.rooms.get_one_or_none(id=room_id)
    booking_data = {"room_id": room_id, "date_from": date_from, "date_to": date_to}
    response = await auth_ac.post("/bookings", json=booking_data)
    response_dict = response.json()
    if response.status_code == 200:
        assert response.status_code == status_code
        assert response_dict["status"] =="OK"
        assert response_dict["data"]["room_id"] == room_id
        assert response_dict["data"]["price"] == room.price


@pytest.fixture(scope="session")
async def test_delete_all_bookings(setup_database):
    async with db_session(session_factory=async_session_maker) as session_db:
        await  session_db.bookings.delete()
        await session_db.commit()

@pytest.mark.parametrize("room_id, date_from, date_to, count", [
    (1, "2025-01-05", "2025-01-10", 1),
    (1, "2025-01-06", "2025-01-11", 2),
    (1, "2025-01-07", "2025-01-12", 3)
])
async def test_add_and_get_my_bookings(test_delete_all_bookings, room_id, date_from, date_to, count, auth_ac):
    booking_data = {"room_id": room_id, "date_from": date_from, "date_to": date_to}
    await auth_ac.post("/bookings", json=booking_data)
    response = await auth_ac.get("/bookings/me")
    response_dict = response.json()
    assert response.status_code == 200
    assert response_dict["status"] == "OK"
    assert len(response_dict["data"]) == count
