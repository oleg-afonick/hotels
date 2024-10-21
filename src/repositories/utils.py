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


async def update_rooms_comforts(db, room_id, room_data):
    comforts = await db.rooms_comforts.get_all_with_filter(room_id=room_id)
    current_comfort_ids = [comfort.comfort_id for comfort in comforts]
    if room_data.comfort_ids:
        comforts_delete = await db.rooms_comforts.get_all_with_filter(
            RoomsComfortsModel.comfort_id.not_in(
                room_data.comfort_ids
            ),
            room_id=room_id
        )
        if comforts_delete:
            for com_del in comforts_delete:
                await db.rooms_comforts.delete(room_id=com_del.room_id, comfort_id=com_del.comfort_id)
        add_comfort_ids = []
        for comfort_id in room_data.comfort_ids:
            if comfort_id not in current_comfort_ids:
                add_comfort_ids.append(comfort_id)
        if add_comfort_ids:
            comfort_data = [
                RoomComfortSchemaPostPut(
                    room_id=room_id,
                    comfort_id=comfort_id
                ) for comfort_id in add_comfort_ids
            ]
            await db.rooms_comforts.add_multiple(comfort_data)
