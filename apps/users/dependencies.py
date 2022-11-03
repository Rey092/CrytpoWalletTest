# -*- coding: utf-8 -*-
from async_lru import alru_cache
from boto3 import Session
from botocore.client import Config
from fastapi_helper.utilities.password_helper import PasswordHelper

from apps.users.database import UserDatabase
from apps.users.jwt_backend import JWTBackend
from apps.users.manager import UserManager
from apps.users.models import Permission, User
from config.db import SessionLocal
from config.settings import settings
from config.storage import SqlAlchemyStorage


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@alru_cache()
async def get_jwt_backend() -> JWTBackend:
    return JWTBackend(settings.jwt_access_expiration)


@alru_cache()
async def get_user_db() -> UserDatabase:
    return UserDatabase(User, Permission)


@alru_cache()
async def get_s3_client():
    session = Session()
    return session.client(
        "s3",
        config=Config(s3={"addressing_style": "virtual"}),
        region_name=settings.spaces_region_name,
        endpoint_url=str(settings.storage_url),
        aws_access_key_id=settings.spaces_access_key,
        aws_secret_access_key=settings.spaces_secret_key,
    )


@alru_cache()
async def get_storage() -> SqlAlchemyStorage:
    s3_client = await get_s3_client()
    return SqlAlchemyStorage(s3_client, settings.spaces_space_name)


@alru_cache()
async def get_user_manager() -> UserManager:
    password_helper = PasswordHelper()
    jwt_backend = await get_jwt_backend()
    user_db = await get_user_db()
    storage = await get_storage()
    return UserManager(user_db, jwt_backend, password_helper, storage)
