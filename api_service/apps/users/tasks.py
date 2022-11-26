# -*- coding: utf-8 -*-
import asyncio
from time import sleep

from celery import current_task
from pydantic import UUID4
from sqlalchemy.orm import Session

from api_service.apps.users.manager import UserManager
from api_service.config.celery import celery_app


async def update_permission(user_id: UUID4, db: Session, user_manager: UserManager):
    await asyncio.sleep(60)
    await user_manager.update_permission(user_id, db)


@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    for i in range(1, 11):
        sleep(1)
        current_task.update_state(
            state="PROGRESS",
            meta={"process_percent": i * 10},
        )
    return f"test task return {word}"
