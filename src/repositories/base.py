from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel
from src.database import engine


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        model = result.scalars().all()
        return [self.schema.model_validate(obj, from_attributes=True) for obj in model]

    async def get_all_with_filter(self, **filter_by):
        query = select(self.model).filter_by(**filter_by).order_by(self.model.id)
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        model = result.scalars().all()
        return [self.schema.model_validate(obj, from_attributes=True) for obj in model]

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        return self.schema.model_validate(model, from_attributes=True) if model else None

    async def add(self, data: BaseModel, **filter_by):
        insert_stmt = insert(self.model).values(**data.model_dump(), **filter_by).returning(self.model)
        print(insert_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(insert_stmt)
        model = result.scalars().one()
        return self.schema.model_validate(model, from_attributes=True)

    async def update(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        update_stmt = update(self.model).filter_by(**filter_by).values(**data.model_dump(exclude_unset=exclude_unset))
        print(update_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await self.session.execute(update_stmt)

    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by)
        print(delete_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await self.session.execute(delete_stmt)
