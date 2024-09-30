from pydantic import BaseModel


class HotelSchema(BaseModel):
    name: str
    address: str


class HotelSchemaPATCH(BaseModel):
    name: str | None = None
    address: str | None = None
