from celery import Celery

from src.config import settings

app = Celery(
    'tasks',
    broker=settings.REDIS_URL,
    include=[
        "src.tasks.celery_tasks",
    ]
)
app.conf.broker_connection_retry_on_startup = True

app.conf.beat_schedule = {
    'periodic_task': {
        'task': 'get_bookings_checkin_today',
        'schedule': 10,
        'args': ()
    }
}
