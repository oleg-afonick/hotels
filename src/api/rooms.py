from fastapi import Body, APIRouter

from src.api.dependencies import db_session
from src.schemas.rooms import RoomSchemaRequest, RoomSchemaPostPut, RoomSchemaPatchRequest, RoomSchemaPatch
from src.api.examples import rooms_example

router = APIRouter(prefix="/hotels", tags=["Комнаты"])


@router.get("/{hotel_id}/rooms/")
async def get_rooms(db: db_session, hotel_id: int):
    return await db.rooms.get_all_with_filter(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(db: db_session, hotel_id: int, room_id: int):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms/")
async def post_room(db: db_session, hotel_id: int, room_data: RoomSchemaRequest = Body(openapi_examples=rooms_example)):
    _room_data = RoomSchemaPostPut(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    await db.commit()

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def put_room(db: db_session, hotel_id: int, room_id: int, room_data: RoomSchemaRequest):
    _room_data = RoomSchemaPostPut(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.update(_room_data, id=room_id)
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
    await db.commit()
    return {"status": "OK"}
