from datetime import date

from fastapi import Body, APIRouter, Query, HTTPException
from fastapi_cache.decorator import cache

from services.rooms import RoomService
from src.api.dependencies import db_session
from src.schemas.rooms import RoomSchemaRequest, RoomSchemaPostPut, RoomSchemaPatchRequest, RoomSchemaPatch
from src.api.examples import rooms_example
from src.exceptions import (
    DateFromLaterDateToException,
    HotelNotFoundException,
    RoomNotFoundException,
    HotelNotFoundHTTPException,
    DateFromLaterDateToHTTPException,
    RoomNotFoundHTTPException,
)

router = APIRouter(prefix="/hotels", tags=["Комнаты"])


@router.get("/{hotel_id}/rooms/")
@cache(expire=30)
async def get_rooms(
        db: db_session,
        hotel_id: int,
        date_from: date = Query(example="2024-10-17"),
        date_to: date = Query(example="2024-10-21"),
):
    try:
        return await RoomService(db).get_rooms(hotel_id, date_from, date_to)
    except DateFromLaterDateToException:
        raise DateFromLaterDateToHTTPException


@router.get("/{hotel_id}/rooms/{room_id}")
@cache(expire=30)
async def get_room(db: db_session, hotel_id: int, room_id: int):
    try:
        return await RoomService(db).get_room(hotel_id, room_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.post("/{hotel_id}/rooms/")
async def post_room(
        db: db_session,
        hotel_id: int,
        room_data: RoomSchemaRequest = Body(openapi_examples=rooms_example)
):
    try:
        room = await RoomService(db).post_room(hotel_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def put_room(db: db_session, hotel_id: int, room_id: int, room_data: RoomSchemaRequest):
    try:
        await RoomService(db).put_room(hotel_id, room_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_room(db: db_session, hotel_id: int, room_id: int, room_data: RoomSchemaPatchRequest):
    try:
        await RoomService(db).patch_room(hotel_id, room_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(db: db_session, hotel_id: int, room_id: int):
    try:
        await RoomService(db).delete_room(hotel_id, room_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    await db.commit()
    return {"status": "OK"}
