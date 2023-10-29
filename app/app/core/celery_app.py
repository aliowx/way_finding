from celery import Celery

from app.core.config import settings


BROKER_URL = (
    f"amqp://{settings.RABBITMQ_USERNAME}:"
    f"{settings.RABBITMQ_PASSWORD}@"
    f"{settings.RABBITMQ_HOST}:"
    f"{settings.RABBITMQ_PORT}"
)


celery_app = Celery(
    "worker", backend="rpc://", broker=BROKER_URL, include=["celery.worker"]
)

celery_app.conf.update(task_track_started=True, broker_connection_retry_on_startup=True)
