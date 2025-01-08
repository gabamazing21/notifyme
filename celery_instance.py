from celery import Celery, Task
from flask import Flask
import os

# Configure celery broker (Redis) and result backend
redis_url = os.getenv("CELERY_BROKER_URL")
CELERY_BROKER_URL = f"{redis_url}?ssl_cert_reqs=required"
CELERY_RESULT_BACKEND = f"{redis_url}?ssl_cert_reqs=required"
def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)
    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.conf.update(
        {"broker_url":CELERY_BROKER_URL,
         "result_backend":CELERY_RESULT_BACKEND,
         "task_ignore_result": True,
         "timezone":"Africa/Lagos"
         })
    celery_app.set_default()
