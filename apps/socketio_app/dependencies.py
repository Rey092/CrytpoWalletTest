# -*- coding: utf-8 -*-
from async_lru import alru_cache

from apps.socketio_app.client_dispatcher import ClientDispatcher
from apps.socketio_app.database import ChatDatabase
from apps.socketio_app.manager import ChatManager
from apps.socketio_app.models import ChatMessage, ChatUser


@alru_cache()
async def get_client_dispatcher() -> ClientDispatcher:
    return ClientDispatcher()


@alru_cache()
async def get_chat_database() -> ChatDatabase:
    return ChatDatabase(ChatUser, ChatMessage)


@alru_cache()
async def get_chat_manager() -> ChatManager:
    database = await get_chat_database()
    return ChatManager(database)
