from sqlalchemy import select

from src.database import engine
from src.repositories.base import BaseRepository
from src.models.comforts import ComfortsModel, RoomsComfortsModel
from src.schemas.comforts import RoomSchema, RoomComfortSchema


class ComfortsRepository(BaseRepository):
    model = ComfortsModel
    schema = RoomSchema


class RoomsComfortsRepository(BaseRepository):
    model = RoomsComfortsModel
    schema = RoomComfortSchema

