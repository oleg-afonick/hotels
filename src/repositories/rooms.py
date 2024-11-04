from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from src.models.comforts import RoomsComfortsModel
from src.mappers.mappers import RoomMapper, RoomM2MMapper
from src.repositories.utils import available_rooms
from src.database import engine
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsModel
from src.schemas.rooms import RoomSchema


class RoomsRepository(BaseRepository):
    model = RoomsModel
    mapper = RoomMapper

    async def get_all_available_rooms(self, *args, **filter_by):
        query = available_rooms(*args).options(selectinload(self.model.comforts)).filter_by(**filter_by).order_by(
            self.model.id)
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        model = result.scalars().all()
        return [RoomM2MMapper.map_to_domain_entity(obj) for obj in model]

    async def get_room_with_comforts(self, **filter_by):
        query = select(self.model).options(selectinload(self.model.comforts)).filter_by(**filter_by)
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        return RoomM2MMapper.map_to_domain_entity(model) if model else None

    async def delete(self, hotel_id, room_id) -> None:
        delete_m2m = delete(RoomsComfortsModel).filter_by(room_id=room_id)
        await self.session.execute(delete_m2m)
        delete_stmt = delete(self.model).filter_by(hotel_id=hotel_id, id=room_id)
        print(delete_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await self.session.execute(delete_stmt)
