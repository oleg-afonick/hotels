from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey


class ComfortsModel(Base):
    __tablename__ = 'comforts'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))

    rooms: Mapped[list['RoomsModel']] = relationship(secondary='rooms_comforts', back_populates='comforts')


class RoomsComfortsModel(Base):
    __tablename__ = 'rooms_comforts'
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id'))
    comfort_id: Mapped[int] = mapped_column(ForeignKey('comforts.id'))
