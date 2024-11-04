from celery import Celery

from src.config import settings

app = Celery(
    'tasks',
    broker=settings.REDIS_URL,
    include=[
        "src.tasks.celery_tasks",
    ]
)

app.conf.beat_schedule = {
    'periodic_task': {
        'task': 'src.tasks.celery_tasks.periodic_task',
        'schedule': 5,
        'args': ()
    }
}
