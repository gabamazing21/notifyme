from celery import Celery, Task
from flask import Flask
import os
import ssl
from dotenv import load_dotenv

# Configure celery broker (Redis) and result backend
load_dotenv()
redis_url = os.getenv("CELERY_BROKER_URL")
CELERY_BROKER_URL = redis_url
CELERY_RESULT_BACKEND = redis_url
def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)
    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.conf.update(
        {"broker_url":CELERY_BROKER_URL,
         "broker_connection_retry_on_startup": True,
         "result_backend":CELERY_RESULT_BACKEND,
         "task_ignore_result": True,
         "timezone":"Africa/Lagos",
         "broker_use_ssl": {
             "ssl_cert_reqs": ssl.CERT_REQUIRED  # Change to "CERT_REQUIRED" for strict SSL verification
            }
         })
    celery_app.set_default()
    return celery_app
