# -*- coding: utf-8 -*-
from async_lru import alru_cache

from apps.socketio_app.client_dispatcher import ClientDispatcher


@alru_cache()
async def get_client_dispatcher() -> ClientDispatcher:
    return ClientDispatcher()
