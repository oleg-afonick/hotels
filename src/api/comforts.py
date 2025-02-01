from fastapi import Body, APIRouter
from fastapi_cache.decorator import cache

from services.comforts import ComfortsService
from src.api.examples import comforts_example

from src.api.dependencies import db_session
from src.schemas.comforts import ComfortSchemaPostPut

router = APIRouter(prefix="/comforts", tags=["Удобства"])


@router.get("")
@cache(expire=30)
async def get_comforts(db: db_session):
    return await ComfortsService(db).get_comforts()


@router.post("")
async def post_comfort(db: db_session, comfort_data: ComfortSchemaPostPut = Body(openapi_examples=comforts_example)):
    comfort = await  ComfortsService(db).post_comfort(comfort_data)
    await db.commit()
    return {"status": "OK", "data": comfort}
