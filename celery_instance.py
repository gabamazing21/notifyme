from celery import Celery
# Configure celery broker (Redis) and result backend
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

celery_app = Celery(
        __name__,
        backend=CELERY_RESULT_BACKEND,
        broker=CELERY_BROKER_URL
    )
celery_app.conf.update({
    "broker_url": CELERY_BROKER_URL,
    "result_backend": CELERY_RESULT_BACKEND})
celery_app.autodiscover_tasks(["tasks"])
