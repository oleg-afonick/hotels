from pydantic import BaseModel


class RoomSchemaRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int


class RoomSchemaPostPut(RoomSchemaRequest):
    hotel_id: int


class RoomSchema(RoomSchemaPostPut):
    id: int

    class Config:
        from_attributes = True


class RoomSchemaPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None


class RoomSchemaPatch(RoomSchemaPatchRequest):
    hotel_id: int | None = None
