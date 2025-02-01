import shutil
from pathlib import Path

from src.tasks.celery_tasks import upload_resize_image_task
from src.services.base import BaseService

# Папка, в которую будут сохраняться загруженные файлы
UPLOAD_DIR = Path("src/static/images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class ImagesService(BaseService):

    @staticmethod
    async def upload_file(file, filename):
        save_name = filename if filename else file.filename
        new_name = f"{save_name.replace(' ', '-')}.jpg"
        file_location = UPLOAD_DIR / f"{new_name}"

        with file_location.open("wb+") as buffer:
            shutil.copyfileobj(file.file, buffer)

        upload_resize_image_task.delay(str(file_location), new_name)

        return new_name
