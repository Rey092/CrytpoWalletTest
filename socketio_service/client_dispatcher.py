# -*- coding: utf-8 -*-
import asyncio
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
        print("The connection failed!")
        print(data)

    @staticmethod
    @sio.event
    async def disconnect():
        print("I'm disconnected!")

    async def sio_connect(self):
        try:
            await sio.connect(self.url, socketio_path="/ws/socket.io")
        except Exception as ex:
            print(ex)

    @staticmethod
    async def sio_disconnect():
        await sio.sleep(1)
        await sio.disconnect()

    @sio.event
    async def new_transactions(self, data: List[dict]):
        await self.sio_connect()
        await sio.emit("new_transactions", data)
        await self.sio_disconnect()

    @sio.event
    async def update_balance(self, data: dict):
        await self.sio_connect()
        await sio.emit("update_balance", data)
        await self.sio_disconnect()

    @sio.event
    async def new_product(self, data: dict):
        await self.sio_connect()
        await sio.emit("new_product", data)
        await self.sio_disconnect()

    @sio.event
    async def new_order(self, data: dict):
        await self.sio_connect()
        await sio.emit("new_order", data)
        await self.sio_disconnect()


if __name__ == "__main__":
    client_manager = ClientDispatcher()
    #     asyncio.run(
    #         client_manager.new_transactions(
    #             [
    #                 {
    #                     "address_to": "0x5744ad47599f9900E55a0eAd25ea0c7237640938",
    #                     "txn_hash": "0xc736da81e45aed442b272e20a9b3e0e3164e0745a297baf566295f99916f7b82",
    #                     "value": 0.5,
    #                     "new_balance": 2.51925653,
    #                 },
    #             ],
    #         ),
    #     )
    asyncio.run(client_manager.new_product({"wallet_id": "66c5aea0-25e6-432c-a1e8-1ff3951fde06", "value": "10"}))
