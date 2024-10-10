from fastapi import Body, APIRouter

from src.schemas.rooms import RoomSchemaPostPut, RoomSchemaPatch
from src.api.examples import rooms_example
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository

router = APIRouter(prefix="/hotels", tags=["Комнаты"])


@router.get("/{hotel_id}/rooms/")
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms/")
async def post_room(hotel_id: int, room_data: RoomSchemaPostPut = Body(openapi_examples=rooms_example)):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data, hotel_id=hotel_id)
        await session.commit()

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def put_rooms(hotel_id: int, room_id: int,  hotel_data: RoomSchemaPostPut):
    async with async_session_maker() as session:
        await RoomsRepository(session).update(data=hotel_data, hotel_id=hotel_id, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_rooms(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(hotel_id=hotel_id, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_rooms(
        hotel_id: int, room_id: int,  hotel_data: RoomSchemaPatch):
    async with async_session_maker() as session:
        await RoomsRepository(session).update(data=hotel_data, hotel_id=hotel_id, id=room_id, exclude_unset=True)
        await session.commit()
    return {"status": "OK"}
