from schemas.comforts import ComfortSchemaPostPut
from src.services.base import BaseService
from src.tasks.celery_tasks import digit_task


class ComfortsService(BaseService):
    async def get_comforts(self):
        # digit_task.delay(10)
        return await self.db.comforts.get_all()

    async def post_comfort(self, comfort_data: ComfortSchemaPostPut):
        comfort = await self.db.comforts.add(comfort_data)
        await self.db.commit()
        return comfort
