# -*- coding: utf-8 -*-
from async_lru import alru_cache
from boto3 import Session
from botocore.client import Config

from socketio_service.apps.chat.database import ChatDatabase
from socketio_service.apps.chat.manager import ChatManager
from socketio_service.apps.chat.models import ChatMessage, ChatUser
from socketio_service.apps.chat.storage import MongoStorage
from socketio_service.client_dispatcher import ClientDispatcher
from socketio_service.config.settings import settings


@alru_cache()
async def get_client_dispatcher() -> ClientDispatcher:
    return ClientDispatcher()


@alru_cache()
async def get_chat_database() -> ChatDatabase:
    return ChatDatabase(ChatUser, ChatMessage)


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
async def get_storage() -> MongoStorage:
    s3_client = await get_s3_client()
    return MongoStorage(s3_client, settings.spaces_space_name)


@alru_cache()
async def get_chat_manager() -> ChatManager:
    database = await get_chat_database()
    storage = await get_storage()
    return ChatManager(database, storage)
