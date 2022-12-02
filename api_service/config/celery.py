# -*- coding: utf-8 -*-
from celery import Celery

import services  # noqa
from api_service.config.settings import settings

celery_app = Celery(
    "worker",
    backend=str(settings.redis_url),
    broker=str(settings.redis_url),
)

celery_app.conf.update(task_track_started=True)
celery_app.autodiscover_tasks(["api_service.apps.users.tasks"])
