from sqlalchemy import select

from src.schemas.hotels import HotelSchema
from src.database import engine
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsModel


class HotelsRepository(BaseRepository):
    model = HotelsModel
    schema = HotelSchema

    async def get_all(self, title, location, limit, offset):
        query = select(self.model).order_by(self.model.id)
        if location:
            query = query.filter(HotelsModel.location.icontains(location))
        if title:
            query = query.filter(HotelsModel.title.icontains(title))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        model = result.scalars().all()
        return [self.schema.model_validate(obj, from_attributes=True) for obj in model]



