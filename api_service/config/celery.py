# -*- coding: utf-8 -*-
from celery import Celery

from api_service.config.settings import settings

celery_app = Celery(
    "worker",
    backend=str(settings.redis_url),
    broker=str(settings.redis_url),
)


# celery_app.conf.update(task_track_started=True)
# celery_app.autodiscover_tasks(["apps.users.tasks"])

# @celery_app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     pass
# Executes every Monday morning at 7:30 a.m.
# sender.add_periodic_task(
#     crontab(minute="*"),
#     save_balance_task.s(),
# )
