from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel
from database import engine


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        insert_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        print(insert_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(insert_stmt)
        return result.scalars().one()

    async def update(self, data: BaseModel, **filter_by):
        update_stmt = update(self.model).filter_by(**filter_by).values(**data.model_dump())
        print(update_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await self.session.execute(update_stmt)

    async def delete(self, **filter_by):
        delete_stmt = delete(self.model).filter_by(**filter_by)
        print(delete_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await self.session.execute(delete_stmt)
