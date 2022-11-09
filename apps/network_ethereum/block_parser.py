# -*- coding: utf-8 -*-
import asyncio
import datetime
import json

from aio_pika import DeliveryMode, ExchangeType, Message, connect_robust
from websockets import connect

from config.settings import settings


async def get_event():
    async with connect(settings.infura_api_url) as websocket:
        await websocket.send(
            '{"jsonrpc": "2.0", "id": 1, "method": "eth_subscribe", "params": ["newHeads"]}',
        )
        subscription_response = await websocket.recv()
        print(f"Parser start successfully {subscription_response}")

        while True:
            try:
                message = await asyncio.wait_for(websocket.recv(), timeout=2)
                response = json.loads(message)
                block_number = response["params"]["result"]["number"]
                print(
                    f'{datetime.datetime.now().strftime("%H:%M:%S")} '
                    f"-- Got new block form Ethereum Network -- {block_number}",
                )

                connection = await connect_robust("amqp://guest:guest@localhost/")

                async with connection:
                    channel = await connection.channel()

                    new_blocks_exchange = await channel.declare_exchange(
                        "new_blocks",
                        ExchangeType.FANOUT,
                    )

                    message = Message(
                        f"{block_number}".encode(),
                        delivery_mode=DeliveryMode.PERSISTENT,
                    )

                    # Sending the message
                    await new_blocks_exchange.publish(message, routing_key="info")

            except Exception:
                pass


if __name__ == "__main__":
    asyncio.run(get_event())
