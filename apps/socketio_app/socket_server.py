# -*- coding: utf-8 -*-
import socketio

from apps.socketio_app.dependencies import get_chat_manager
from apps.socketio_app.models import ChatMessage

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")


@sio.event
async def connect(sid, environ, auth):
    print("connect")
    await sio.save_session(sid, {"auth": auth, "sid": sid})
    session = await sio.get_session(sid)
    manager = await get_chat_manager()
    history = await manager.get_history_chat()
    await sio.emit("get_history", {"history": history, "user": session}, room=sid)
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


# region IBay
@sio.event
async def new_product(sid, data):
    await sio.emit("front_new_product", data)


@sio.event
async def new_order(sid, data):
    await sio.emit("front_new_order", data)


# endregion IBay


# region Chat
@sio.event
async def new_message(sid, data):
    manager = await get_chat_manager()
    message = ChatMessage(**data)
    await manager.new_message(message)
    session = await sio.get_session(sid)
    await sio.emit("update_message", {"message": data, "user": session})


# @sio.event
# async def list_messages(sid):
#     manager = await get_chat_manager()
#     history = await manager.get_history_chat()
#     session = await sio.get_session(sid)
#     await sio.emit('get_history', {"history": history, "user": session})


@sio.event
async def writes_message(sid, data):
    print("writes_message", data)
    await sio.emit("writes_message", {"sid": sid})


# endregion Chat
