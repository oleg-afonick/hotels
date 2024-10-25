from sqlalchemy import select, insert, delete

from src.database import engine
from src.repositories.base import BaseRepository
from src.models.comforts import ComfortsModel, RoomsComfortsModel
from src.schemas.comforts import ComfortSchema, RoomComfortSchema


class ComfortsRepository(BaseRepository):
    model = ComfortsModel
    schema = ComfortSchema


class RoomsComfortsRepository(BaseRepository):
    model = RoomsComfortsModel
    schema = RoomComfortSchema

    async def set_room_comforts(self, room_id: int, comfort_ids: list[int]):
        query = select(self.model.comfort_id).filter_by(room_id=room_id)
        result = await self.session.execute(query)
        current_comfort_ids = result.scalars().all()

        insert_comfort_ids = list(set(comfort_ids) - set(current_comfort_ids))
        delete_comfort_ids = list(set(current_comfort_ids) - set(comfort_ids))

        if insert_comfort_ids:
            insert_stmt = insert(self.model).values(
                [{'room_id': room_id, 'comfort_id': c_id} for c_id in insert_comfort_ids])
            print(insert_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
            await self.session.execute(insert_stmt)

        if delete_comfort_ids:
            delete_stmt = delete(self.model).where(self.model.room_id == room_id,
                                                   self.model.comfort_id.in_(delete_comfort_ids))
            print(delete_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
            await self.session.execute(delete_stmt)
