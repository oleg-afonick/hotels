from datetime import date

from src.exceptions import HotelNotFoundException, RoomNotFoundException
from src.schemas.comforts import RoomComfortSchemaPostPut
from src.schemas.rooms import RoomSchemaRequest, RoomSchemaPostPut, RoomSchemaPatchRequest, RoomSchemaPatch
from src.services.base import BaseService


class RoomService(BaseService):

    async def check_for_update_room(self, room_data, room_id, exclude_unset=False):
        try:
            await self.db.rooms.update_room(room_data, id=room_id, exclude_unset=exclude_unset)
        except HotelNotFoundException:
            raise HotelNotFoundException
        except RoomNotFoundException:
            raise RoomNotFoundException

    async def post_room(
            self,
            hotel_id: int,
            room_data: RoomSchemaRequest
    ):
        _room_data = RoomSchemaPostPut(hotel_id=hotel_id, **room_data.model_dump())
        room = await self.db.rooms.add_room(_room_data)
        if room_data.comfort_ids:
            comfort_data = [
                RoomComfortSchemaPostPut(
                    room_id=room.id,
                    comfort_id=comfort_id
                ) for comfort_id in room_data.comfort_ids
            ]
            await self.db.rooms_comforts.add_multiple(comfort_data)
        await self.db.commit()
        return room

    async def get_rooms(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):
        return await self.db.rooms.get_all_available_rooms(date_from, date_to, hotel_id=hotel_id)

    async def get_room(self, hotel_id: int, room_id: int):
        return await self.db.rooms.get_room_with_comforts(id=room_id, hotel_id=hotel_id)

    async def put_room(self, hotel_id: int, room_id: int, room_data: RoomSchemaRequest):
        _room_data = RoomSchemaPostPut(hotel_id=hotel_id, **room_data.model_dump())
        await self.check_for_update_room(_room_data, room_id)
        await self.db.rooms_comforts.set_room_comforts(room_id, room_data.comfort_ids)
        await self.db.commit()

    async def patch_room(self, hotel_id: int, room_id: int, room_data: RoomSchemaPatchRequest):
        room_data_dict = room_data.model_dump(exclude_unset=True)
        room_data_patch = RoomSchemaPatch(hotel_id=hotel_id, **room_data_dict)
        await self.check_for_update_room(room_data_patch, room_id, exclude_unset=True)
        if 'comfort_ids' in room_data_dict:
            await self.db.rooms_comforts.set_room_comforts(room_id, room_data_dict['comfort_ids'])
        await self.db.commit()

    async def delete_room(self, hotel_id: int, room_id: int):
        try:
            await self.db.rooms.delete_room(hotel_id, room_id)
        except HotelNotFoundException as ex:
            raise HotelNotFoundException
        except RoomNotFoundException as ex:
            raise RoomNotFoundException
        await self.db.commit()
