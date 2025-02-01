from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.services.bookings import BookingService
from src.schemas.bookings import BookingSchemaRequest
from src.api.dependencies import db_session, current_user_id
from src.exceptions import (NoFreeRoomsException, RoomNotFoundException, RoomNotFoundHTTPException,
                            NoFreeRoomsHTTPException, DateFromLaterDateToException, DateFromLaterDateToHTTPException)

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("")
async def post_booking(db: db_session, user_id: current_user_id, booking_data: BookingSchemaRequest):
    try:
        booking = await BookingService(db).post_booking(user_id, booking_data)
    except DateFromLaterDateToException:
        raise DateFromLaterDateToHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except NoFreeRoomsException:
        raise NoFreeRoomsHTTPException

    return {"status": "OK", "data": booking}


@router.get("")
@cache(expire=30)
async def get_bookings(db: db_session):
    bookings = await BookingService(db).get_bookings()
    return {"status": "OK", "data": bookings}


@router.get("/checkin_today")
@cache(expire=30)
async def get_bookings_checkin_today(db: db_session):
    bookings = await BookingService(db).get_bookings_checkin_today()
    return {"status": "OK", "data": bookings}


@router.get("/me")
async def get_my_bookings(db: db_session, user_id: current_user_id):
    bookings = await BookingService(db).get_my_bookings(user_id)
    return {"status": "OK", "data": bookings}
