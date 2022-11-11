# -*- coding: utf-8 -*-
import asyncio
import json
import logging
from threading import Thread

from aio_pika import connect_robust
from aio_pika.abc import AbstractIncomingMessage, ExchangeType

from apps.ibay.config.db import SessionLocalIBay
from apps.ibay.dependencies import get_ibay_manager
from config.settings import settings

logger = logging.getLogger(__name__)


async def handle_new_order(message: AbstractIncomingMessage) -> None:
    db = SessionLocalIBay()
    ibay_manager = await get_ibay_manager()
    async with message.process():
        logger.info(f"IBay new order: {message.body}")
        await ibay_manager.create_new_order(db, json.loads(message.body.decode("utf-8")))


async def consumer() -> None:
    connection = await connect_robust(settings.rabbit_url)
    async with connection:
        channel = await connection.channel()

        # create exchanges
        new_order_exchange = await channel.declare_exchange(
            "new_order_exchange",
            ExchangeType.FANOUT,
        )

        # Declaring queue
        new_order_queue = await channel.declare_queue(exclusive=True)

        # Binding the queue to the exchange
        await new_order_queue.bind(new_order_exchange)

        # Start listening the queue
        await new_order_queue.consume(handle_new_order)

        logger.info("[*] Waiting for messages from API service")
        await asyncio.Future()


ibay_consumer_thread = Thread(target=asyncio.run, args=(consumer(),))
