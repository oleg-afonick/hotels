from datetime import date

from fastapi import Body, APIRouter, Query

from src.repositories.utils import update_rooms_comforts
from src.schemas.comforts import RoomComfortSchemaPostPut
from src.api.dependencies import db_session
from src.schemas.rooms import RoomSchemaRequest, RoomSchemaPostPut, RoomSchemaPatchRequest, RoomSchemaPatch
from src.api.examples import rooms_example

router = APIRouter(prefix="/hotels", tags=["Комнаты"])


@router.get("/{hotel_id}/rooms/")
async def get_rooms(
        db: db_session,
        hotel_id: int,
        date_from: date = Query(example="2024-10-17"),
        date_to: date = Query(example="2024-10-21"),
        ):
    return await db.rooms.get_all_available_rooms(date_from, date_to, hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(db: db_session, hotel_id: int, room_id: int):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms/")
async def post_room(
        db: db_session,
        hotel_id: int,
        room_data: RoomSchemaRequest = Body(openapi_examples=rooms_example)
):
    _room_data = RoomSchemaPostPut(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    comfort_data = [
        RoomComfortSchemaPostPut(
            room_id=room.id,
            comfort_id=comfort_id
        ) for comfort_id in room_data.comfort_ids
    ]
    await db.rooms_comforts.add_multiple(comfort_data)
    await db.commit()

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def put_room(db: db_session, hotel_id: int, room_id: int, room_data: RoomSchemaRequest):
    _room_data = RoomSchemaPostPut(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.update(_room_data, id=room_id)
    await update_rooms_comforts(db, room_id, room_data)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(db: db_session, hotel_id: int, room_id: int):
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_room(db: db_session, hotel_id: int, room_id: int, room_data: RoomSchemaPatchRequest):
    _room_data = RoomSchemaPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.update(_room_data, id=room_id, exclude_unset=True)
    await update_rooms_comforts(db, room_id, room_data)
    await db.commit()
    return {"status": "OK"}
