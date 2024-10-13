from typing import Annotated

from fastapi import Query, Depends, Request, HTTPException

from pydantic import BaseModel

from src.database import async_session_maker
from src.services.auth import auth_service
from src.utils.db_manager import DatabaseManager


class Paginator(BaseModel):
    page: Annotated[int | None, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(None, ge=1, le=20)]


paginator = Annotated[Paginator, Depends()]


def get_access_token(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Пользователь не аутентифицирован")
    return access_token


def get_current_user_id(access_token: str = Depends(get_access_token)):
    data = auth_service.decode_access_token(access_token)
    user_id = data.get("user_id")
    return user_id


current_user_id = Annotated[int, Depends(get_current_user_id)]


async def get_db():
    async with DatabaseManager(session_factory=async_session_maker) as db:
        yield db


db_session = Annotated[DatabaseManager, Depends(get_db)]
