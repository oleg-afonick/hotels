from fastapi import APIRouter, Body, HTTPException, Response

from src.exceptions import ExistsEmailException
from src.api.dependencies import current_user_id, db_session
from src.services.auth import auth_service

from src.api.examples import users_example
from src.schemas.users import UserSchemaRequestAdd, UserSchemaAdd

router = APIRouter(prefix="/auth", tags=["Регистрация и аутентификация"])


@router.post("/register")
async def register_user(db: db_session, data: UserSchemaRequestAdd = Body(openapi_examples=users_example)):
    if not data.password:
        raise HTTPException(status_code=422, detail="Введите пароль")
    hashed_password = auth_service.hashed_password(data.password)
    user_database = UserSchemaAdd(email=data.email, hashed_password=hashed_password)
    try:
        await db.users.add_user(user_database)
    except ExistsEmailException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    await db.commit()
    return {"status": "OK"}



@router.post("/login")
async def login_user(db: db_session, response: Response,
                     data: UserSchemaRequestAdd = Body(openapi_examples=users_example)):
    user = await db.users.get_user_for_login(email=data.email)
    if not user:
        return HTTPException(status_code=409, detail="Пользователь с таким email не существует")
    if not auth_service.verify_password(data.password, user.hashed_password):
        return HTTPException(status_code=409, detail="Неверный пароль")
    access_token = auth_service.create_access_token({"user_id": user.id})
    response.set_cookie(key="access_token", value=access_token)

    return {"access_token": access_token}


@router.get("/current_user")
async def current_user(db: db_session, user_id: current_user_id):
    user = await db.users.get_one_or_none(id=user_id)

    return user


@router.get("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")

    return {"status": "OK"}
