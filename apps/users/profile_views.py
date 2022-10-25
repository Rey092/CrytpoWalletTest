# -*- coding: utf-8 -*-
from fastapi import APIRouter
from pydantic import UUID4

from apps.users.manager import get_user_manager

profile_router = APIRouter()


@profile_router.get("/")
async def get_profile(id: UUID4):
    manager = await get_user_manager()
    user = await manager.get_user(id)
    return user


@profile_router.put("/")
async def update_profile(id: UUID4):
    manager = await get_user_manager()
    user = await manager.get_user(id)
    return user
