from sqlalchemy import select

from src.database import engine
from src.repositories.base import BaseRepository
from src.models.comforts import ComfortsModel
from src.schemas.comforts import RoomSchema


class ComfortsRepository(BaseRepository):
    model = ComfortsModel
    schema = RoomSchema
