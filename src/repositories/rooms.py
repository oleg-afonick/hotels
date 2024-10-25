from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.repositories.utils import available_rooms
from src.database import engine
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsModel
from src.schemas.rooms import RoomSchema


class RoomsRepository(BaseRepository):
    model = RoomsModel
    schema = RoomSchema

    async def get_all_available_rooms(self, *args, **filter_by):
        query = available_rooms(*args).options(selectinload(self.model.comforts)).filter_by(**filter_by).order_by(
            self.model.id)
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        model = result.scalars().all()
        return [self.schema.model_validate(obj, from_attributes=True) for obj in model]

    async def get_room_with_comforts(self, **filter_by):
        query = select(self.model).options(selectinload(self.model.comforts)).filter_by(**filter_by)
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        return self.schema.model_validate(model, from_attributes=True) if model else None
