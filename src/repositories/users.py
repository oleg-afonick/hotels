from pydantic import EmailStr
from sqlalchemy import select

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
