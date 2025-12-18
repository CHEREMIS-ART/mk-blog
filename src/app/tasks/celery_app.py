from celery import Celery

from src.app.core.config import settings

celery_app = Celery(
    "blog_tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.task_routes = {
    "src.app.tasks.email.send_registration_email": {"queue": "emails"},
}
