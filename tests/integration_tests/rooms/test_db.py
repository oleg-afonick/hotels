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
    await db.commit()
    assert new_booking

    get_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert get_booking

    update_booking_data =BookingSchemaPostPut(
        user_id=booking_data.user_id,
        room_id=booking_data.room_id,
        date_from=booking_data.date_from,
        date_to=booking_data.date_to,
        price=5555
    )
    await db.bookings.update(id=new_booking.id, data=update_booking_data)
    await db.commit()
    get_booking_update = await db.bookings.get_one_or_none(id=new_booking.id)
    assert get_booking_update.price == 5555

    await db.bookings.delete(id=new_booking.id)
    await db.commit()
    get_booking_delete = await db.bookings.get_one_or_none(id=new_booking.id)
    assert not get_booking_delete
