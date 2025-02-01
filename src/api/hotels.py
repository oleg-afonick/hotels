from datetime import date

from fastapi import Body, Query, APIRouter
from fastapi_cache.decorator import cache

from src.services.hotels import HotelService
from src.api.examples import hotels_example
from src.api.dependencies import paginator, db_session
from src.schemas.hotels import HotelSchemaPostPut, HotelSchemaPatch
from src.exceptions import (
    DateFromLaterDateToException,
    ObjectNotFoundException,
    HotelNotFoundHTTPException,
    DateFromLaterDateToHTTPException,
)

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=30)
async def get_hotels(
        db: db_session,
        pagination: paginator,
        date_from: date = Query(example="2024-10-17"),
        date_to: date = Query(example="2024-10-21"),
        location: str | None = Query(None, description="Адрес отеля"),
        title: str | None = Query(None, description="Название отеля"),
):
    try:
        return await HotelService(db).get_all_with_available_rooms(
            pagination,
            date_from,
            date_to,
            location,
            title
        )
    except DateFromLaterDateToException:
        raise DateFromLaterDateToHTTPException


@router.get("/{hotel_id}")
@cache(expire=30)
async def get_hotel(db: db_session, hotel_id: int, ):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.post("")
async def post_hotel(db: db_session, hotel_data: HotelSchemaPostPut = Body(openapi_examples=hotels_example)):
    hotel = await HotelService(db).post_hotel(hotel_data)
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def put_hotel(db: db_session, hotel_id: int, hotel_data: HotelSchemaPostPut):
    await HotelService(db).put_hotel(hotel_id, hotel_data)
    return {"status": "OK"}


@router.patch("/{hotel_id}")
async def patch_hotel(db: db_session, hotel_id: int, hotel_data: HotelSchemaPatch):
    await HotelService(db).patch_hotel(hotel_id, hotel_data)
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(db: db_session, hotel_id: int):
    await HotelService(db).delete_hotel(hotel_id)
    return {"status": "OK"}
