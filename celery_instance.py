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
         "result_backend": None,
         "task_ignore_result": True,
         "timezone":"Africa/Lagos",
         # reduce command per day because of upstash
         "task_acks_late": True, # Acknowledge tasks after completion
         "task_default_retry_delay": 10, # Retry delay in seconds
         "max_retries": 3, # Limit retries per task
         "task_always_eager": False,
         "broker_transport_options": {
             "visibility_timeout": 3000,
         },
         "worker_send_task_events": False,
         "worker_prefetch_multiplier": 1,
         "broker_heartbeat": 30,
         "worker_log_format": "%(asctime)s - %(levelname)s - %(message)s",
         # optional debugging logs
         "broker_use_ssl": {
             "ssl_cert_reqs": ssl.CERT_REQUIRED
            }
         })
    celery_app.set_default()
    return celery_app
