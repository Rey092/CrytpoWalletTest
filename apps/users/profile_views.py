# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.orm import Session

from apps.users.dependencies import get_db, get_user_manager
from apps.users.manager import UserManager

profile_router = APIRouter()


@profile_router.get("/")
async def get_profile(
    user_id: UUID4,
    user_manager: UserManager = Depends(get_user_manager),
    db: Session = Depends(get_db),
):
    user = await user_manager.get_user(user_id, db)
    return user


@profile_router.put("/")
async def update_profile(
    user_id: UUID4,
    user_manager: UserManager = Depends(get_user_manager),
    db: Session = Depends(get_db),
):
    user = await user_manager.get_user(user_id, db)
    return user
