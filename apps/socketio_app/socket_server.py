# -*- coding: utf-8 -*-
import socketio

# mgr = socketio.AsyncAioPikaManager('amqp://guest:guest@localhost/', 'new_blocks', logger=True)
sio = socketio.AsyncServer(cors_allowed_origins="*", async_mode="asgi", logger=True, engineio_logger=True)
# app = web.Application()
# sio.attach(app)


@sio.event
async def connect(sid, environ, auth):
    print("connect", sid)


@sio.event
async def new_transaction(sid, data):
    print(data)


@sio.event
async def update_balance(sid, data):
    print(data)


@sio.event
async def new_blocks(sid, data):
    print(sid)
    print(data)


@sio.event
async def disconnect(sid):
    print("disconnect", sid)


# if __name__ == '__main__':
#     web.run_app(app, host='localhost', port=5000)
