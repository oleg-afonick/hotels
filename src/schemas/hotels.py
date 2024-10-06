from pydantic import BaseModel


class HotelSchemaPostPut(BaseModel):
    title: str
    location: str


class HotelSchema(HotelSchemaPostPut):
    id: int


class HotelSchemaPatch(BaseModel):
    title: str | None = None
    location: str | None = None
