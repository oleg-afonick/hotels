from pydantic import BaseModel

from src.schemas.comforts import ComfortSchemaPostPut


class RoomSchemaRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    comfort_ids: list[int] = []


class RoomSchemaPostPut(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int


class RoomSchema(RoomSchemaPostPut):
    id: int


class RoomM2MSchema(RoomSchemaPostPut):
    id: int
    comforts: list[ComfortSchemaPostPut]


class RoomSchemaPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    comfort_ids: list[int] = []


class RoomSchemaPatch(BaseModel):
    hotel_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
