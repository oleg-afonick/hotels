from datetime import date

from src.schemas.hotels import HotelSchemaPostPut, HotelSchemaPatch
from src.services.base import BaseService

class HotelService(BaseService):
    async def get_all_with_available_rooms(
            self,
            pagination,
            date_from: date,
            date_to: date,
            location: str | None,
            title: str | None,
    ):
        per_page = pagination.per_page or 5
        return await self.db.hotels.get_all_with_available_rooms(
            date_from,
            date_to,
            title=title,
            location=location,
            limit=per_page,
            offset=(pagination.page - 1) * per_page
        )


    async def get_hotel(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def post_hotel(self, hotel_data: HotelSchemaPostPut):
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return hotel

    async def put_hotel(self, hotel_id: int, hotel_data: HotelSchemaPostPut):
        await self.db.hotels.update(id=hotel_id, data=hotel_data)
        await self.db.commit()

    async def patch_hotel(self, hotel_id: int, hotel_data: HotelSchemaPatch):
        await self.db.hotels.update(id=hotel_id, exclude_unset=True, data=hotel_data)
        await self.db.commit()

    async def delete_hotel(self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()