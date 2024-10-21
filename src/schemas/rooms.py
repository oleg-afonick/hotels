from pydantic import BaseModel


class RoomSchemaRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    comfort_ids: list[int] | None = None


class RoomSchemaPostPut(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int


class RoomSchema(RoomSchemaPostPut):
    id: int

    class Config:
        from_attributes = True


class RoomSchemaPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    comfort_ids: list[int] | None = None


class RoomSchemaPatch(BaseModel):
    hotel_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
