from fastapi import Body, Query, APIRouter

from src.database import async_session_maker, engine
from src.api.dependencies import paginator
from src.schemas.hotels import HotelSchema, HotelSchemaPATCH
from sqlalchemy import insert, select
from src.models.hotels import HotelsModel

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("")
async def get_hotels(
        pagination: paginator,
        location: str | None = Query(None, description="Адрес отеля"),
        title: str | None = Query(None, description="Название отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsModel)
        if location:
            query = query.filter(HotelsModel.location.icontains(location))
        if title:
            query = query.filter(HotelsModel.title.icontains(title))
        query = (
            query
            .limit(per_page)
            .offset((pagination.page - 1) * per_page)
        )
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels


@router.post("")
async def post_hotels(hotel_data: HotelSchema = Body(openapi_examples={
    "1": {
        "summary": "Сочи",
        "value": {
            "title": "Отель 5 звезд у Черного моря",
            "location": "Сочи, ул. Моря, 1"
        }
    },
    "2": {
        "summary": "Дубай",
        "value": {
            "title": "Отель 5 звезд в Персидском заливе",
            "location": "Дубай, ул. Шейха, 2"
        }
    }
})):
    async with async_session_maker() as session:
        insert_hotel_stmt = insert(HotelsModel).values(**hotel_data.model_dump())
        print(insert_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(insert_hotel_stmt)
        await session.commit()

    return {"status": "OK"}


# @router.put("/{hotel_id}")
# def hotels_put(hotel_id: int, hotel_data: HotelSchema):
#     get_hotel = [hotel for hotel in hotels if hotel.get("id") == hotel_id]
#     if get_hotel:
#         hotel = get_hotel[0]
#         hotel["name"] = hotel_data.name
#         hotel["address"] = hotel_data.address
#         return hotels
#     return "Hotel not found"
#
#
# @router.patch("/{hotel_id}")
# def hotels_patch(
#         hotel_id: int, hotel_data: HotelSchemaPATCH):
#     get_hotel = [hotel for hotel in hotels if hotel.get("id") == hotel_id]
#     if get_hotel:
#         hotel = get_hotel[0]
#         hotel["name"] = hotel_data.name if hotel_data.name else hotel["name"]
#         hotel["address"] = hotel_data.address if hotel_data.address else hotel["address"]
#         return hotels
#     return "Hotel not found"
#
#
# @router.delete("/{hotel_id}")
# def hotels_delete(hotel_id: int):
#     get_hotel = [hotel for hotel in hotels if hotel.get("id") == hotel_id]
#     if get_hotel:
#         hotel = get_hotel[0]
#         hotels.remove(hotel)
#         return hotels
#     return "Hotel not found"
