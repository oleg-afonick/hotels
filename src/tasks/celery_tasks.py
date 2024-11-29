import asyncio
from time import sleep
from celery import shared_task
from PIL import Image
from pathlib import Path

from src.database import async_session_maker_null_pool
from src.utils.db_manager import DatabaseManager
from src.tasks.email_sender import send_email

RESIZE_DIMENSIONS = [200, 500, 1000]


@shared_task
def digit_task(n):
    for number in range(1, n + 1):
        sleep(1)
        print(number)
    print("Задача выполнена")


@shared_task
def upload_resize_image_task(image_path, file_name):
    file_location = Path(image_path)
    try:
        with Image.open(file_location) as img:
            # Пробегаемся по всем указанным размерам и сохраняем каждый вариант
            for size in RESIZE_DIMENSIONS:
                # Создаем копию изображения, изменяем его размер и сохраняем
                resized_img = img.copy()
                resized_img.thumbnail((size, size))

                # Генерируем имя для измененного изображения
                resized_file_location = f"src/static/images/{file_location.stem}_{size}px{file_location.suffix}"
                resized_img.save(resized_file_location)

    except Exception as e:
        return {"error": f"Произошла ошибка при обработке изображения: {str(e)}"}

    return {"info": f"Файл '{file_name}' успешно загружен и сохранен в размерах 200, 500 и 1000 пикселей"}


async def get_bookings_checkin_today_helper():
    async with DatabaseManager(session_factory=async_session_maker_null_pool) as db:
        bookings = await db.bookings.get_bookings_checkin_today()
        for booking in bookings:
            room = await db.rooms.get_one_or_none(id=booking.room_id)
            user = await db.users.get_one_or_none(id=booking.user_id)
            subject = "Напоминание о заезде"
            username = user.email.split('@')[0].capitalize()
            user_email = user.email
            body = f"Здравствуйте, {username}! Сегодня у вас заезд в комнату '{room.title}'. Хорошего отдыха!"
            send_email(subject, body, user_email)


@shared_task(name="get_bookings_checkin_today")
def bookings_checkin_today_task():
    asyncio.run(get_bookings_checkin_today_helper())
