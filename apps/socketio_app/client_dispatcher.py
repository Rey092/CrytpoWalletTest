# -*- coding: utf-8 -*-
import asyncio
from typing import List

import socketio

sio = socketio.AsyncClient()


@sio.event
async def message(data):
    print(data)
    print("I received a message!")


# @sio.on('*')
# async def catch_all(event, data):
#     print('Универсальный обработчик событий')
#     print(event)
#     print(data)


class ClientDispatcher:
    url = "http://127.0.0.1:8000"

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
        await sio.connect(self.url, socketio_path="/ws/socket.io")

    @staticmethod
    async def sio_disconnect():
        await sio.sleep(1)
        await sio.disconnect()

    @sio.event
    async def new_transactions(self, data: List[dict]):
        try:
            await self.sio_connect()
        except Exception as ex:
            print(ex)
        await sio.emit("new_transactions", data)
        await self.sio_disconnect()

    @sio.event
    async def update_balance(self, data: dict):
        try:
            await self.sio_connect()
        except Exception as ex:
            print(ex)
        await sio.emit("update_balance", data)
        await self.sio_disconnect()


if __name__ == "__main__":
    client_manager = ClientDispatcher()
    asyncio.run(
        client_manager.new_transactions(
            [
                {
                    "address_to": "0x5744ad47599f9900E55a0eAd25ea0c7237640938",
                    "txn_hash": "0xc736da81e45aed442b272e20a9b3e0e3164e0745a297baf566295f99916f7b82",
                    "value": 0.5,
                    "new_balance": 2.51925653,
                },
            ],
        ),
    )
    # asyncio.run(client_manager.update_balance({"wallet_id": "66c5aea0-25e6-432c-a1e8-1ff3951fde06", "value": "10"}))
