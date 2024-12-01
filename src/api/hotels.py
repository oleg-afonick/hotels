from datetime import date

from fastapi import Body, Query, APIRouter
from fastapi_cache.decorator import cache

from src.api.examples import hotels_example

from src.api.dependencies import paginator, db_session
from src.schemas.hotels import HotelSchemaPostPut, HotelSchemaPatch

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
    per_page = pagination.per_page or 5

    return await db.hotels.get_all_with_available_rooms(
        date_from,
        date_to,
        title=title,
        location=location,
        limit=per_page,
        offset=(pagination.page - 1) * per_page
    )


@router.get("/{hotel_id}")
@cache(expire=30)
async def get_hotel(db: db_session, hotel_id: int,):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post("")
async def post_hotel(db: db_session, hotel_data: HotelSchemaPostPut = Body(openapi_examples=hotels_example)):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def put_hotel(db: db_session, hotel_id: int, hotel_data: HotelSchemaPostPut):
    await db.hotels.update(id=hotel_id, data=hotel_data)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(db: db_session, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}")
async def patch_hotel(db: db_session, hotel_id: int, hotel_data: HotelSchemaPatch):
    await db.hotels.update(id=hotel_id, exclude_unset=True, data=hotel_data)
    await db.commit()
    return {"status": "OK"}
