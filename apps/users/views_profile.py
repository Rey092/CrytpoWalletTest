# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from apps.users.dependencies import get_db, get_user_manager
from apps.users.manager import UserManager
from apps.users.models import User
from apps.users.user import get_current_user

profile_router = APIRouter()


@profile_router.get("/")
async def get_profile(
    user=Depends(get_current_user),
):
    return user


@profile_router.put("/")
async def update_profile(
    user: User = Depends(get_current_user),
    user_manager: UserManager = Depends(get_user_manager),
    db: Session = Depends(get_db),
):
    return user
