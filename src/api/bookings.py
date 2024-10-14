from fastapi import APIRouter, Body

from src.schemas.bookings import BookingSchemaRequest, BookingSchemaPostPut
from src.api.dependencies import db_session, current_user_id

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("")
async def post_booking(
        db: db_session,
        user_id: current_user_id,
        booking_data: BookingSchemaRequest
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    price: int = room.price
    _booking_data = BookingSchemaPostPut(user_id=user_id, price=price, **booking_data.model_dump())
    booking = await db.bookings.add(_booking_data)
    await db.commit()

    return {"status": "OK", "data": booking}


@router.get("")
async def get_bookings(db: db_session):
    bookings = await db.bookings.get_all()
    return {"status": "OK", "data": bookings}


@router.get("/me")
async def get_my_bookings(
        db: db_session,
        user_id: current_user_id
):
    bookings = await db.bookings.get_all_with_filter(user_id=user_id)
    return {"status": "OK", "data": bookings}

