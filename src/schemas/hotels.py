from pydantic import BaseModel


class HotelSchemaPostPut(BaseModel):
    title: str
    location: str


class HotelSchema(BaseModel):
    id: int
    title: str
    location: str


class HotelSchemaPatch(BaseModel):
    title: str | None = None
    location: str | None = None
