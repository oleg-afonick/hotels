from pydantic import BaseModel
from sqlalchemy import select, delete, insert, update
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.orm import selectinload

from src.models.hotels import HotelsModel
from src.models.comforts import RoomsComfortsModel
from src.mappers.mappers import RoomMapper, RoomM2MMapper
from src.repositories.utils import available_rooms
from src.database import engine
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsModel
from src.exceptions import DateFromLaterDateToException, HotelNotFoundException, RoomNotFoundException


class RoomsRepository(BaseRepository):
    model = RoomsModel
    mapper = RoomMapper

    async def get_all_available_rooms(self, *args, **filter_by):
        date_from, date_to = args
        if date_from > date_to:
            raise DateFromLaterDateToException
        query = available_rooms(*args).options(selectinload(self.model.comforts)).filter_by(**filter_by).order_by(
            self.model.id)
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        model = result.scalars().all()
        return [RoomM2MMapper.map_to_domain_entity(obj) for obj in model]

    async def get_room_with_comforts(self, **filter_by):
        try:
            hotel = select(HotelsModel).filter_by(id=filter_by["hotel_id"])
            result = await self.session.execute(hotel)
            result.scalar_one()
        except NoResultFound:
            raise HotelNotFoundException
        query = select(self.model).options(selectinload(self.model.comforts)).filter_by(**filter_by)
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
            return RoomM2MMapper.map_to_domain_entity(model) if model else None
        except NoResultFound:
            raise RoomNotFoundException

    async def add_room(self, data: BaseModel, **filter_by):
        insert_stmt = insert(self.model).values(**data.model_dump(), **filter_by).returning(self.model)
        print(insert_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        try:
            result = await self.session.execute(insert_stmt)
            model = result.scalar_one()
            return self.mapper.map_to_domain_entity(model)
        except IntegrityError:
            raise HotelNotFoundException

    async def update_room(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        try:
            hotel = select(HotelsModel).filter_by(id=data.hotel_id)
            result = await self.session.execute(hotel)
            result.scalar_one()
        except NoResultFound:
            raise HotelNotFoundException

        try:
            room = select(self.model).filter_by(id=filter_by["id"])
            result = await self.session.execute(room)
            result.scalar_one()
        except NoResultFound:
            raise RoomNotFoundException

        update_stmt = update(self.model).filter_by(**filter_by).values(**data.model_dump(exclude_unset=exclude_unset))
        print(update_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await self.session.execute(update_stmt)

    async def delete_room(self, hotel_id, room_id) -> None:
        try:
            hotel = select(HotelsModel).filter_by(id=hotel_id)
            result = await self.session.execute(hotel)
            result.scalar_one()
        except NoResultFound:
            raise HotelNotFoundException

        try:
            room = select(self.model).filter_by(id=room_id)
            result = await self.session.execute(room)
            result.scalar_one()
        except NoResultFound:
            raise RoomNotFoundException

        delete_m2m = delete(RoomsComfortsModel).filter_by(room_id=room_id)
        await self.session.execute(delete_m2m)
        delete_stmt = delete(self.model).filter_by(hotel_id=hotel_id, id=room_id)
        print(delete_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await self.session.execute(delete_stmt)
