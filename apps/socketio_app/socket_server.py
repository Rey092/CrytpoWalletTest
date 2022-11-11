# -*- coding: utf-8 -*-
import socketio

from apps.socketio_app.dependencies import get_chat_database
from apps.socketio_app.models import ChatMessage

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")


@sio.event
async def connect(sid, environ, auth):
    print("connect")
    await sio.save_session(sid, {"auth": auth, "sid": sid})
    session = await sio.get_session(sid)
    await sio.emit("connect_user", session)


@sio.event
async def disconnect(sid):
    print("disconnect")
    data = {"sid": sid}
    await sio.emit("disconnect_user", data)


# region Wallets
@sio.event
async def new_transactions(sid, data):
    await sio.emit("front_new_transactions", data)


@sio.event
async def update_balance(sid, data):
    await sio.emit("front_update_wallet_balance", data)


# endregion Wallets


# region Chat
@sio.event
async def new_message(sid, data):
    print("message", data)
    mongodb_chat = await get_chat_database()
    mes = ChatMessage(**data)
    await mongodb_chat.create_message(mes)
    session = await sio.get_session(sid)
    await sio.emit("update_message", {"message": data, "user": session})


@sio.event
async def writes_message(sid, data):
    print("writes_message", data)
    await sio.emit("writes_message", data)


# endregion Chat
