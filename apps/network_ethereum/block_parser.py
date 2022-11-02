# -*- coding: utf-8 -*-
import asyncio
import json
import logging

import aio_pika
from websockets import connect

from config.settings import settings

logger = logging.getLogger(__name__)


async def get_event():
    async with connect(settings.infura_api_url) as websocket:
        await websocket.send(
            '{"jsonrpc": "2.0", "id": 1, "method": "eth_subscribe", "params": ["newHeads"]}',
        )
        subscription_response = await websocket.recv()
        logger.info(f"Parser start successfully {subscription_response}")

        while True:
            try:
                message = await asyncio.wait_for(websocket.recv(), timeout=2)
                response = json.loads(message)
                block_number = response["params"]["result"]["number"]

                connection = await aio_pika.connect_robust(
                    settings.rabbit_url,
                )
                async with connection:
                    routing_key = "new_block"
                    channel = await connection.channel()

                    await channel.default_exchange.publish(
                        aio_pika.Message(body=f"{block_number}".encode()),
                        routing_key=routing_key,
                    )
            except Exception:
                pass
