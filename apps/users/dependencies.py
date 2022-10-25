# -*- coding: utf-8 -*-
from async_lru import alru_cache
from fastapi_helper.utilities.password_helper import PasswordHelper

from apps.users.database import UserDatabase
from apps.users.jwt_backend import JWTBackend
from apps.users.manager import UserManager
from apps.users.models import Permission, User
from config.settings import settings


@alru_cache()
async def get_jwt_backend() -> JWTBackend:
    return JWTBackend(settings.jwt_access_expiration)


@alru_cache()
async def get_user_db() -> UserDatabase:
    return UserDatabase(User, Permission)


@alru_cache()
async def get_user_manager() -> UserManager:
    password_helper = PasswordHelper()
    jwt_backend = await get_jwt_backend()
    user_db = await get_user_db()
    return UserManager(user_db, jwt_backend, password_helper)
