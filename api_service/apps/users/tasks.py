# -*- coding: utf-8 -*-
import asyncio

from api_service.apps.users.dependencies import get_user_manager
from api_service.config import celery_app
from api_service.config.db import SessionLocal


@celery_app.task
def update_permission(user_id):
    print("Task send")
    db = SessionLocal()
    try:
        user_manager = asyncio.run(get_user_manager())
        asyncio.run(user_manager.update_permission(user_id, db))
    except Exception as exc:
        print(exc)
    finally:
        db.close()
    print("Task completed")
