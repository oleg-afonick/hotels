from pydantic import BaseModel


class ComfortSchemaPostPut(BaseModel):
    title: str


class RoomSchema(ComfortSchemaPostPut):
    id: int

    class Config:
        from_attributes = True


class RoomComfortSchemaPostPut(BaseModel):
    room_id: int
    comfort_id: int


class RoomComfortSchema(RoomComfortSchemaPostPut):
    id: int

    class Config:
        from_attributes = True
