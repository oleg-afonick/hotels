from src.exceptions import (ObjectNotFoundException, RoomNotFoundException,
                            NoFreeRoomsException, DateFromLaterDateToException)
from src.api.dependencies import current_user_id
from src.schemas.bookings import BookingSchemaRequest, BookingSchemaPostPut
from src.services.base import BaseService


class BookingService(BaseService):

    async def get_bookings(self):
        return await self.db.bookings.get_all()

    async def get_bookings_checkin_today(self):
        return await self.db.bookings.get_bookings_checkin_today()

    async def get_my_bookings(self, user_id: current_user_id):
        return await self.db.bookings.get_all_with_filter(user_id=user_id)

    async def post_booking(self, user_id: current_user_id, booking_data: BookingSchemaRequest):
        if booking_data.date_from > booking_data.date_to:
            raise DateFromLaterDateToException
        try:
            room = await self.db.rooms.get_one(id=booking_data.room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException
        price: int = room.price
        _booking_data = BookingSchemaPostPut(user_id=user_id, price=price, **booking_data.model_dump())
        try:
            booking = await self.db.bookings.add_booking(_booking_data)
        except NoFreeRoomsException:
            raise NoFreeRoomsException
        await self.db.commit()
        return booking
