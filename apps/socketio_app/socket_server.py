# -*- coding: utf-8 -*-
import socketio

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")


@sio.event
async def connect(sid, environ, auth):
    print("connect", sid)
    data = {"sid": sid, "auth": auth}
    await sio.emit("connect_user", data)


@sio.event
async def disconnect(sid):
    print("disconnect", sid)
    data = {"sid": sid}
    await sio.emit("disconnect_user", data)


# region Wallets
@sio.event
async def new_transaction(sid, data):
    print(data)
    await sio.emit("new_transaction", data)


@sio.event
async def update_balance(sid, data):
    print(data)
    await sio.emit("front_update_wallet_balance", data)


# endregion Wallets


# region Chat
@sio.event
async def new_message(sid, data):
    print("message", data)
    await sio.emit("update_message", data)


@sio.event
async def writes_message(sid, data):
    print("writes_message", data)
    await sio.emit("writes_message", data)


# endregion Chat
