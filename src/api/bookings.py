from fastapi import APIRouter, Body

from src.api.examples import bookings_example
from src.schemas.bookings import BookingSchemaRequest, BookingSchemaPostPut
from src.api.dependencies import db_session, current_user_id

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("")
async def post_booking(db: db_session, user_id: current_user_id, booking_data: BookingSchemaRequest = Body(openapi_examples=bookings_example)):
    room_id = booking_data.model_dump().get("room_id")
    room = await db.rooms.get_one_or_none(id=room_id)
    price = room.price
    _booking_data = BookingSchemaPostPut(user_id=user_id, price=price, **booking_data.model_dump())
    booking = await db.bookings.add(_booking_data)
    await db.commit()

    return {"status": "OK", "data": booking}
