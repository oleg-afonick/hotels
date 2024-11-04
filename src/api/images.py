from fastapi import APIRouter, UploadFile, Form
import shutil
from pathlib import Path

from src.tasks.celery_tasks import upload_resize_image_task

router = APIRouter(prefix="/images", tags=["Изображения"])

# Папка, в которую будут сохраняться загруженные файлы
UPLOAD_DIR = Path("src/static/images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
RESIZE_DIMENSIONS = [200, 500, 100]


@router.post("")
async def upload_file(file: UploadFile, filename: str = Form(None)):
    save_name = filename if filename else file.filename
    new_name = f"{save_name.replace(' ', '-')}.jpg"
    file_location = UPLOAD_DIR / f"{new_name}"

    with file_location.open("wb+") as buffer:
        shutil.copyfileobj(file.file, buffer)

    upload_resize_image_task.delay(str(file_location), new_name)

    return {"info": f"Файл '{new_name}' успешно загружен"}
