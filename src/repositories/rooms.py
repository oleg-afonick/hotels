from sqlalchemy import select

from src.database import engine
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsModel
from src.schemas.rooms import RoomSchema


class RoomsRepository(BaseRepository):
    model = RoomsModel
    schema = RoomSchema

