from fastapi import Body, Query, APIRouter

from src.api.examples import comforts_example

from src.api.dependencies import db_session
from src.schemas.comforts import ComfortSchemaPostPut

router = APIRouter(prefix="/comforts", tags=["Удобства"])


@router.get("")
async def get_comforts(db: db_session):
    return await db.comforts.get_all()


@router.post("")
async def post_comfort(db: db_session, comfort_data: ComfortSchemaPostPut = Body(openapi_examples=comforts_example)):
    comfort = await db.comforts.add(comfort_data)
    await db.commit()

    return {"status": "OK", "data": comfort}
