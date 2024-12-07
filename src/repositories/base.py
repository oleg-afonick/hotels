from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel
from sqlalchemy.exc import NoResultFound, IntegrityError

from src.exceptions import ObjectNotFoundException, HotelsException
from src.mappers.base import DataMapper
from src.database import engine


class BaseRepository:
    model = None
    schema: BaseModel = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        model = result.scalars().all()
        return [self.mapper.map_to_domain_entity(obj) for obj in model]

    async def get_all_with_filter(self, *args, **filter_by):
        query = select(self.model).filter_by(**filter_by).filter(*args).order_by(self.model.id)
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        model = result.scalars().all()
        return [self.mapper.map_to_domain_entity(obj) for obj in model]

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
            return self.mapper.map_to_domain_entity(model) if model else None
        except NoResultFound:
            raise ObjectNotFoundException


    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        return self.mapper.map_to_domain_entity(model) if model else None

    async def add(self, data: BaseModel, **filter_by):
        insert_stmt = insert(self.model).values(**data.model_dump(), **filter_by).returning(self.model)
        print(insert_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        try:
            result = await self.session.execute(insert_stmt)
            model = result.scalars().one()
            return self.mapper.map_to_domain_entity(model)
        except IntegrityError:
            raise HotelsException

    async def add_multiple(self, data: list[BaseModel]):
        insert_stmt = insert(self.model).values([item.model_dump() for item in data])
        print(insert_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await self.session.execute(insert_stmt)

    async def update(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        update_stmt = update(self.model).filter_by(**filter_by).values(**data.model_dump(exclude_unset=exclude_unset))
        print(update_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await self.session.execute(update_stmt)

    async def delete(self, *args, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by).filter(*args)
        print(delete_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await self.session.execute(delete_stmt)
