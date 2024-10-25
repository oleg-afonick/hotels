from sqlalchemy import select, func

from src.models.comforts import RoomsComfortsModel
from src.schemas.comforts import RoomComfortSchemaPostPut
from src.models.hotels import HotelsModel
from src.models.rooms import RoomsModel

from src.models.bookings import BookingsModel


def available_rooms(date_from, date_to):
    rooms_ids = (
        select(BookingsModel.room_id)
        .select_from(RoomsModel)
        .join(BookingsModel, BookingsModel.room_id == RoomsModel.id)
        .filter(BookingsModel.date_from <= date_to, BookingsModel.date_to >= date_from)
        .group_by(BookingsModel.room_id, RoomsModel.quantity)
        .having(RoomsModel.quantity - func.coalesce(func.count(BookingsModel.room_id), 0) == 0)
    ).cte(name='available_rooms')

    query = (
        select(RoomsModel)
        .select_from(RoomsModel)
        .filter(RoomsModel.id.not_in(select(rooms_ids.c.room_id).select_from(rooms_ids)))
    )
    return query


def hotels_with_available_rooms(date_from, date_to):
    a_rooms = available_rooms(date_from, date_to)

    hotels_available_rooms_ids = (
        select(a_rooms.c.hotel_id).select_from(a_rooms)
        .subquery(name='hotels_available_rooms_ids')
    )
    query = select(HotelsModel).select_from(HotelsModel).filter(HotelsModel.id.in_(hotels_available_rooms_ids))
    return query





