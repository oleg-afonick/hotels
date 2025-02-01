from fastapi import APIRouter, UploadFile, Form

from src.services.images import ImagesService

router = APIRouter(prefix="/images", tags=["Изображения"])


@router.post("")
async def upload_file(file: UploadFile, filename: str = Form(None)):
    new_name = await ImagesService().upload_file(file, filename)

    return {"info": f"Файл '{new_name}' успешно загружен"}
