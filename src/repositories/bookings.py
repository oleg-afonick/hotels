from pydantic import BaseModel
from sqlalchemy import select, insert

from src.database import engine
from src.repositories.base import BaseRepository
from src.models.bookings import BookingsModel
from src.schemas.bookings import BookingSchema


class BookingsRepository(BaseRepository):
    model = BookingsModel
    schema = BookingSchema

    async def get_all(self, **filter_by):
        query = select(self.model).filter_by(**filter_by).order_by(self.model.id)

        print(query.compile(engine, compile_kwargs={"literal_binds": True}))

        result = await self.session.execute(query)
        model = result.scalars().all()
        return [self.schema.model_validate(obj, from_attributes=True) for obj in model]