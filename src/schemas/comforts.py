from pydantic import BaseModel


class ComfortSchemaPostPut(BaseModel):
    title: str


class ComfortSchema(ComfortSchemaPostPut):
    id: int


class RoomComfortSchemaPostPut(BaseModel):
    room_id: int
    comfort_id: int


class RoomComfortSchema(RoomComfortSchemaPostPut):
    id: int
