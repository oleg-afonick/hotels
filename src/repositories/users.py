from src.schemas.users import UserSchema
from src.repositories.base import BaseRepository
from src.models.users import UsersModel


class UsersRepository(BaseRepository):
    model = UsersModel
    schema = UserSchema
