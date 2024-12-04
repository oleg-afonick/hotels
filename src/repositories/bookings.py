from datetime import date

from fastapi import HTTPException
from pendulum import today
from sqlalchemy import select
from pydantic import BaseModel
from sqlalchemy import insert

from schemas.rooms import RoomM2MSchema
from src.models import RoomsModel
from src.mappers.mappers import BookingMapper, RoomM2MMapper
from src.database import engine
from src.repositories.base import BaseRepository
from src.models.bookings import BookingsModel
from src.repositories.utils import available_rooms
from sqlalchemy.orm import selectinload


class BookingsRepository(BaseRepository):
    model = BookingsModel
    mapper = BookingMapper

    async def get_all(self, **filter_by):
        query = select(self.model).filter_by(**filter_by).order_by(self.model.id)

        print(query.compile(engine, compile_kwargs={"literal_binds": True}))

        result = await self.session.execute(query)
        model = result.scalars().all()
        return [self.mapper.map_to_domain_entity(obj) for obj in model]

    async def get_bookings_checkin_today(self):
        query = select(self.model).filter(self.model.date_from == date.today()).order_by(self.model.id)

        print(query.compile(engine, compile_kwargs={"literal_binds": True}))

        result = await self.session.execute(query)
        model = result.scalars().all()
        return [self.mapper.map_to_domain_entity(obj) for obj in model]


    async def add_booking(self, data: BaseModel, **filter_by):
        room_id = data.room_id
        date_from = data.date_from
        date_to = data.date_to

        query = select(RoomsModel).filter_by(id=room_id)
        result = await self.session.execute(query)
        hotel_id = result.scalars().one_or_none().hotel_id

        query = available_rooms(date_from, date_to).filter_by(hotel_id=hotel_id)
        result = await self.session.execute(query)
        rooms = result.scalars().all()

        if room_id in [room.id for room in rooms]:
            insert_stmt = insert(self.model).values(**data.model_dump(), **filter_by).returning(self.model)
            print(insert_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
            result = await self.session.execute(insert_stmt)
            model = result.scalars().one()
            return self.mapper.map_to_domain_entity(model)
        else:
            raise HTTPException(status_code=500, detail="Нет свободных комнат!")