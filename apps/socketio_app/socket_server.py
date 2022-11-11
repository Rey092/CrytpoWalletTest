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
    print("message", data)
    await sio.emit("update_message", data)


@sio.event
async def writes_message(sid, data):
    print("writes_message", data)
    await sio.emit("writes_message", data)


# endregion Chat
