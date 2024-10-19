from src.repositories.utils import available_rooms
from src.database import engine
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsModel
from src.schemas.rooms import RoomSchema


class RoomsRepository(BaseRepository):
    model = RoomsModel
    schema = RoomSchema

    async def get_all_available_rooms(self, *args, **filter_by):
        query = available_rooms(*args).filter_by(**filter_by).order_by(self.model.id)
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        model = result.scalars().all()
        return [self.schema.model_validate(obj, from_attributes=True) for obj in model]
