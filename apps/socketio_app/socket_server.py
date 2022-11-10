# -*- coding: utf-8 -*-
import socketio

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")


@sio.event
async def connect(sid, environ, auth):
    print("connect", sid)


@sio.event
async def disconnect(sid):
    print("disconnect", sid)


# region Wallets
@sio.event
async def new_transactions(sid, data):
    await sio.emit("front_new_transactions", data)


@sio.event
async def update_balance(sid, data):
    await sio.emit("front_update_wallet_balance", data)


# endregion Wallets


# region Chat
@sio.event()
async def new_message(sid, data):
    print("message", data)
    await sio.emit("update_message", data)


# endregion Chat
