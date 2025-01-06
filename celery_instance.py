from celery import Celery
# Configure celery broker (Redis) and result backend
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"


celery_app = Celery(
        __name__,
        backend=CELERY_RESULT_BACKEND,
        broker=CELERY_BROKER_URL)

celery_app.conf.update({
    "broker":CELERY_BROKER_URL,
    "backend":CELERY_RESULT_BACKEND
})

    # class ContextTask(celery_app.Task):
    #     """ Task class that pushes Flask app context"""
    #     def __call__(self, *args, **kwargs):
    #         with flask_app.app_context():
    #             return self.run(*args, **kwargs)
    
    # celery_app.Task = ContextTask
    # return celery_app 