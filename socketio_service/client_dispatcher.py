# -*- coding: utf-8 -*-
from typing import List

import socketio

from socketio_service.config.settings import settings

sio = socketio.AsyncClient()


class ClientDispatcher:
    url = settings.base_host

    @staticmethod
    @sio.event
    async def connect():
        print("I'm connected!")

    @staticmethod
    @sio.event
    async def connect_error(data):
        print(f"The connection failed! from connect_error -- {data}")

    @staticmethod
    @sio.event
    async def disconnect():
        print("I'm disconnected!")

    async def sio_connect(self):
        try:
            await sio.connect(self.url, socketio_path="/ws/socket.io")
        except Exception as ex:
            print(f"This exception from connect in Client Dispatcher -- {str(ex)}")

    @staticmethod
    async def sio_disconnect():
        await sio.disconnect()

    @sio.event
    async def new_transactions(self, data: List[dict]):
        await self.sio_connect()
        await sio.emit("new_transactions", data)

    @sio.event
    async def update_balance(self, data: dict):
        await self.sio_connect()
        await sio.emit("update_balance", data)

    @sio.event
    async def new_product(self, data: dict):
        await self.sio_connect()
        await sio.emit("new_product", data)

    @sio.event
    async def new_order(self, data: dict):
        await self.sio_connect()
        await sio.emit("new_order", data)

    @sio.event
    async def update_order(self, data: dict):
        await self.sio_connect()
        await sio.emit("update_order", data)

    @sio.event
    async def create_user(self, data: dict):
        await self.sio_connect()
        await sio.emit("create_user", data)

    @sio.event
    async def update_user(self, data: dict):
        await self.sio_connect()
        await sio.emit("update_user", data)

    @sio.event
    async def update_permission(self, data: dict):
        await self.sio_connect()
        await sio.emit("update_permission", data)

    @sio.event
    async def returned_transaction(self, data: dict):
        await self.sio_connect()
        await sio.emit("returned_transaction", data)
