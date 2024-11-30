from src.schemas.hotels import HotelSchemaPostPut


async def test_add_hotel(db):
    hotel_data = HotelSchemaPostPut(title="Hotel 5 stars", location="Sochi")
    new_hotel = await db.hotels.add(hotel_data)
    await db.commit()
    print(f"{new_hotel=}")
