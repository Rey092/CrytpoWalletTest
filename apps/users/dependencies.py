# -*- coding: utf-8 -*-
from async_lru import alru_cache
from fastapi_helper.utilities.password_helper import PasswordHelper

from apps.users.manager import UserManager, user_db


@alru_cache()
async def get_user_manager() -> UserManager:
    password_helper = PasswordHelper()
    return UserManager(user_db, password_helper)
