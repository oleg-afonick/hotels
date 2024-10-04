from sqlalchemy import select

from src.database import engine
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsModel


class HotelsRepository(BaseRepository):
    model = HotelsModel

    async def get_all(self, title, location, limit, offset):
        query = select(self.model).order_by(HotelsModel.id)
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
        return result.scalars().all()



