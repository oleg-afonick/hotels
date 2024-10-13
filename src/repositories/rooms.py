from sqlalchemy import select

from src.database import engine
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsModel
from src.schemas.rooms import RoomSchema


class RoomsRepository(BaseRepository):
    model = RoomsModel
    schema = RoomSchema

    async def get_all(self, **filter_by):
        query = select(self.model).filter_by(**filter_by).order_by(self.model.id)

        print(query.compile(engine, compile_kwargs={"literal_binds": True}))

        result = await self.session.execute(query)
        model = result.scalars().all()
        return [self.schema.model_validate(obj, from_attributes=True) for obj in model]
