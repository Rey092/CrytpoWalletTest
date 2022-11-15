# -*- coding: utf-8 -*-
from async_lru import alru_cache

from socketio_service.apps.chat.database import ChatDatabase
from socketio_service.apps.chat.manager import ChatManager
from socketio_service.apps.chat.models import ChatMessage, ChatUser
from socketio_service.client_dispatcher import ClientDispatcher


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
