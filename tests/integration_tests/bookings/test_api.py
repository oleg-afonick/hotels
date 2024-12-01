import json


async def test_add_comforts(db, auth_ac):
    room = (await db.rooms.get_all())[0]
    booking_data = {"room_id": room.id, "date_from": "2025-01-05", "date_to": "2025-01-10"}
    response = await auth_ac.post("/bookings", json=booking_data)
    response_dict = response.json()
    assert response.status_code == 200
    assert response_dict["status"] =="OK"
    assert response_dict["data"]["room_id"] == room.id
    assert response_dict["data"]["price"] == room.price

