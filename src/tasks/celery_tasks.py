from time import sleep
from celery import shared_task
from PIL import Image
from pathlib import Path


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

    return {"info": f"Файл '{file_name}' успешно загружен и сохранен размерах 200, 500 и 1000 пикселей"}


@shared_task
def periodic_task():
    print("Задача выполняется каждые 5 секунд")
