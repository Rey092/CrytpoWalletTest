# -*- coding: utf-8 -*-
import asyncio

from pydantic import UUID4
from sqlalchemy.orm import Session

from apps.users.manager import UserManager


async def update_permission(user_id: UUID4, db: Session, user_manager: UserManager):
    await asyncio.sleep(60)
    await user_manager.update_permission(user_id, db)
