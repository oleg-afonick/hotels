from datetime import date

from pydantic import BaseModel


class BookingSchemaRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingSchemaPostPut(BookingSchemaRequest):
    user_id: int
    price: int


class BookingSchema(BookingSchemaPostPut):
    id: int

    class Config:
        from_attributes = True


class BookingSchemaPatchRequest(BaseModel):
    ...


class BookingSchemaPatch(BookingSchemaPatchRequest):
    ...
