# -*- coding: utf-8 -*-
import asyncio

import socketio
from beanie import init_beanie
from fastapi import FastAPI

from socketio_service.apps.chat.dependencies import get_chat_manager
from socketio_service.config.db import collections, db
from socketio_service.socket_server import sio
from socketio_service.socket_service_consumer import socket_consumer_thread


async def init_mongodb() -> init_beanie:
    await init_beanie(database=db, document_models=collections)


def create_app() -> FastAPI:
    app_ = FastAPI()

    sio_server = socketio.ASGIApp(socketio_server=sio, socketio_path="socket.io")
    app_.mount("/ws", sio_server)  # noqa

    return app_


app = create_app()


@app.on_event("startup")
async def start_mongodb():
    await init_mongodb()
    chat_manager = await get_chat_manager()
    await chat_manager.disconnect_all_users()
    await asyncio.sleep(15)
    socket_consumer_thread.start()


@app.on_event("shutdown")
async def close_mongodb():
    chat_manager = await get_chat_manager()
    await chat_manager.disconnect_all_users()
