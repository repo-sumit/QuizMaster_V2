from flask import current_app as app
from celery import Celery

def create_celery_instance(app):
    celery = Celery(
        app.import_name,
        broker='redis://localhost:6379/0',
        result_backend='redis://localhost:6379/0'
    )
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = create_celery_instance(app)
celery.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='Asia/Kolkata',
        enable_utc=True,
        broker_connection_retry_on_startup=True
    )