# -*- coding: utf-8 -*-
import socketio
from beanie import init_beanie
from fastapi import FastAPI

from socketio_service.config.db import collections, db
from socketio_service.socket_server import sio
from socketio_service.socket_service_consumer import socket_consumer_thread


async def init_mongodb() -> init_beanie:
    await init_beanie(database=db, document_models=collections)


def create_app() -> FastAPI:
    app_ = FastAPI()

    sio_server = socketio.ASGIApp(socketio_server=sio, socketio_path="socket.io")
    app_.mount("/ws", sio_server)  # noqa

    socket_consumer_thread.start()

    return app_


app = create_app()


@app.on_event("startup")
async def start_mongodb():
    await init_mongodb()
