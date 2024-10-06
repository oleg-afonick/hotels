from fastapi import APIRouter, Body

from passlib.context import CryptContext

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserSchemaRequestAdd, UserSchemaAdd

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("register")
async def register_user(data: UserSchemaRequestAdd = Body(openapi_examples={
    "1": {
        "summary": "Пользователь",
        "value": {
            "email": "test@mail.ru",
            "password": "test"
        }
    }
})):
    hashed_password = pwd_context.hash(data.password)
    user_database = UserSchemaAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(user_database)
        await session.commit()

    return {"status": "OK"}
