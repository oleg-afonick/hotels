from datetime import date

from src.schemas.bookings import BookingSchemaPostPut


async def test_booking_crud(db):
    booking_data = BookingSchemaPostPut(
    user_id=(await db.users.get_all())[0].id,
    room_id=(await db.rooms.get_all())[0].id,
    date_from=date(year=2024, month=12, day=10),
    date_to=date(year=2024, month=12, day=20),
    price=100500
    )
    new_booking = await db.bookings.add(booking_data)
    assert new_booking
    assert booking_data.user_id == new_booking.user_id
    assert booking_data.room_id == new_booking.room_id
    assert booking_data.date_from == new_booking.date_from
    assert booking_data.date_to == new_booking.date_to
    assert booking_data.price == new_booking.price

    get_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert get_booking

    update_booking_data =BookingSchemaPostPut(
        user_id=booking_data.user_id,
        room_id=booking_data.room_id,
        date_from=date(year=2024, month=12, day=21),
        date_to=date(year=2024, month=12, day=31),
        price=5555
    )
    await db.bookings.update(id=new_booking.id, data=update_booking_data)

    get_booking_update = await db.bookings.get_one_or_none(id=new_booking.id)
    assert str(get_booking_update.date_from) == "2024-12-21"
    assert str(get_booking_update.date_to) == "2024-12-31"
    assert get_booking_update.price == 5555

    await db.bookings.delete(id=new_booking.id)
    get_booking_delete = await db.bookings.get_one_or_none(id=new_booking.id)
    assert not get_booking_delete
