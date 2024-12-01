from fastapi import Body, Query, APIRouter
from fastapi_cache.decorator import cache

from src.api.examples import comforts_example

from src.api.dependencies import db_session
from src.schemas.comforts import ComfortSchemaPostPut
from src.tasks.celery_tasks import digit_task

router = APIRouter(prefix="/comforts", tags=["Удобства"])


@router.get("")
# @cache(expire=30)
async def get_comforts(db: db_session):
    # digit_task.delay(10)
    return await db.comforts.get_all()


@router.post("")
async def post_comfort(db: db_session, comfort_data: ComfortSchemaPostPut = Body(openapi_examples=comforts_example)):
    comfort = await db.comforts.add(comfort_data)
    await db.commit()

    return {"status": "OK", "data": comfort}
