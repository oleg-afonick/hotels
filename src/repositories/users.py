from pydantic import EmailStr, BaseModel
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError

from src.exceptions import ExistsEmailException
from src.database import engine
from src.mappers.mappers import UserMapper, UserLoginMapper
from src.repositories.base import BaseRepository
from src.models.users import UsersModel


class UsersRepository(BaseRepository):
    model = UsersModel
    mapper = UserMapper

    async def get_user_for_login(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserLoginMapper.map_to_domain_entity(model)

    async def add_user(self, data: BaseModel, **filter_by):
        insert_stmt = insert(self.model).values(**data.model_dump(), **filter_by).returning(self.model)
        print(insert_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        try:
            result = await self.session.execute(insert_stmt)
            model = result.scalars().one()
            return self.mapper.map_to_domain_entity(model)
        except IntegrityError:
            raise ExistsEmailException
