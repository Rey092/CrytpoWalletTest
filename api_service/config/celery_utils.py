# -*- coding: utf-8 -*-
from celery import current_app as current_celery_app
from celery.result import AsyncResult

from api_service.config.settings import settings


def create_celery():
    class CelerySettings:
        CELERY_BROKER_URL: settings.redis_url
        CELERY_RESULT_BACKEND: settings.rabbit_url

    celery_settings = CelerySettings()

    celery_app = current_celery_app
    celery_app.config_from_object(celery_settings, namespace="CELERY")
    celery_app.conf.update(task_track_started=True)
    celery_app.conf.update(task_serializer="json")
    celery_app.conf.update(result_serializer="json")
    celery_app.conf.update(accept_content=["json"])
    celery_app.conf.update(result_persistent=True)
    celery_app.conf.update(worker_send_task_events=False)
    celery_app.conf.update(worker_prefetch_multiplier=1)

    return celery_app


def get_task_info(task_id):
    """
    return task info for the given task_id.
    """
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result,
    }
    return result
