from fastapi import Body, Query, APIRouter

from src.api.examples import hotels_example
from src.database import async_session_maker
from src.api.dependencies import paginator
from src.schemas.hotels import HotelSchema, HotelSchemaPostPut, HotelSchemaPatch
from src.repositories.hotels import HotelsRepository

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
        pagination: paginator,
        location: str | None = Query(None, description="Адрес отеля"),
        title: str | None = Query(None, description="Название отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            title=title,
            location=location,
            limit=per_page,
            offset=(pagination.page - 1) * per_page
        )


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)


@router.post("")
async def post_hotels(hotel_data: HotelSchemaPostPut = Body(openapi_examples=hotels_example)):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def put_hotels(hotel_id: int, hotel_data: HotelSchemaPostPut):
    async with async_session_maker() as session:
        await HotelsRepository(session).update(id=hotel_id, data=hotel_data)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotels(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}")
async def patch_hotels(
        hotel_id: int, hotel_data: HotelSchemaPatch):
    async with async_session_maker() as session:
        await HotelsRepository(session).update(id=hotel_id, exclude_unset=True, data=hotel_data)
        await session.commit()
    return {"status": "OK"}
