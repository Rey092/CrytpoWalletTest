# -*- coding: utf-8 -*-
from async_lru import alru_cache

from apps.socketio_app.client_dispatcher import ClientDispatcher
from apps.socketio_app.database import ChatDatabase


@alru_cache()
async def get_client_dispatcher() -> ClientDispatcher:
    return ClientDispatcher()


@alru_cache()
async def get_chat_database() -> ChatDatabase:
    return ChatDatabase()
