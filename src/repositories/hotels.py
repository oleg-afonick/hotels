from src.repositories.utils import hotels_with_available_rooms
from src.schemas.hotels import HotelSchema
from src.database import engine
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsModel


class HotelsRepository(BaseRepository):
    model = HotelsModel
    schema = HotelSchema

    async def get_all_with_available_rooms(self, date_from, date_to, title, location, limit, offset):
        query = hotels_with_available_rooms(date_from, date_to).order_by(self.model.id)
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
