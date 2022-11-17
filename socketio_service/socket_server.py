# -*- coding: utf-8 -*-

import socketio

from socketio_service.apps.chat.dependencies import get_chat_manager
from socketio_service.apps.chat.models import ChatMessage
from socketio_service.config.utils.service_path import get_path

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")


@sio.event
async def connect(sid, environ, auth):
    await sio.save_session(sid, {"auth": auth, "sid": sid})
    if await get_path(auth):
        sio.enter_room(sid, "chat_users")
        session = await sio.get_session(sid)
        manager = await get_chat_manager()
        # user = ChatUser(
        #     id=session.get('auth').get('id'),
        #     username=session.get('auth').get('username'),
        #     avatar=session.get('auth').get('avatar'),
        #     online=False
        # )
        # await manager.create_user(user)
        await manager.connect_user(session)
        history = await manager.get_history_chat()
        users = await manager.get_online_users()
        await sio.emit("connect_user", session, room="chat_users")
        await sio.emit("get_online_users", users, to=sid)
        await sio.emit("get_history", {"history": history, "user": session}, to=sid)


@sio.event
async def disconnect(sid):
    pass
    # session = await sio.get_session(sid)
    # manager = await get_chat_manager()
    # await manager.disconnect_user(session)
    # await sio.emit(
    #     "disconnect_user",
    #     {"sid": sid},
    #     room="chat_users",
    # )


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


@sio.event
async def update_order(sid, data):
    await sio.emit("front_update_order", data)


# endregion IBay


# region Chat
@sio.event
async def new_message(sid, data):
    manager = await get_chat_manager()
    message_chat = ChatMessage(**data)
    message = await manager.new_message(message_chat)
    session = await sio.get_session(sid)
    await sio.emit(
        "add_message",
        {
            "message": message,
            "user": session,
        },
        room="chat_users",
    )


@sio.event
async def detail_user(sid, data):
    session = await sio.get_session(
        data.get("sid"),
    )
    await sio.emit("data_user", session, room="chat_users", to=sid)


# @sio.event
# async def writes_message(sid, data):
#     await sio.emit(
#         "writes_message",
#         {"sid": sid},
#         room='chat_users'
#     )

# endregion Chat
