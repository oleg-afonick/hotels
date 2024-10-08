from fastapi import APIRouter, Body, HTTPException, Response

from src.api.dependencies import current_user_id
from src.services.auth import auth_service

from src.api.examples import users_example
from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserSchemaRequestAdd, UserSchemaAdd

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.post("/register")
async def register_user(data: UserSchemaRequestAdd = Body(openapi_examples=users_example)):
    hashed_password = auth_service.hashed_password(data.password)
    user_database = UserSchemaAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(user_database)
        await session.commit()

    return {"status": "OK"}


@router.post("/login")
async def login_user(response: Response, data: UserSchemaRequestAdd = Body(openapi_examples=users_example)):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_for_login(email=data.email)
        if not user:
            return HTTPException(status_code=401, detail="Пользователь с таким email не существует")
        if not auth_service.verify_password(data.password, user.hashed_password):
            return HTTPException(status_code=401, detail="Неверный пароль")
        access_token = auth_service.create_access_token({"user_id": user.id})
        response.set_cookie(key="access_token", value=access_token)

    return {"access_token": access_token}


@router.get("/current_user")
async def current_user(user_id: current_user_id):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)

    return user


@router.get("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")

    return {"status": "OK"}
