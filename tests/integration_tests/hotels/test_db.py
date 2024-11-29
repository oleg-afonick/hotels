from src.api.dependencies import db_session
from src.database import async_session_maker_null_pool
from src.schemas.hotels import HotelSchemaPostPut


async def test_add_hotel():
    hotel_data = HotelSchemaPostPut(title ="Hotel 5 stars", location="Sochi")
    async with db_session(session_factory=async_session_maker_null_pool) as db:
        new_hotel = await db.hotels.add(hotel_data)
        await db.commit()
        print(f"{new_hotel=}")
