from pydantic import BaseModel


class RoomSchemaPostPut(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int


class RoomSchema(BaseModel):
    id: int
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int

    class Config:
        from_attributes = True


class RoomSchemaPatch(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
