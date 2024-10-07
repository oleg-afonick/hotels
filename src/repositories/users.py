from pydantic import EmailStr
from sqlalchemy import select

from src.schemas.users import UserSchema, UserSchemaLogin
from src.repositories.base import BaseRepository
from src.models.users import UsersModel


class UsersRepository(BaseRepository):
    model = UsersModel
    schema = UserSchema

    async def get_user_for_login(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserSchemaLogin.model_validate(model, from_attributes=True)

