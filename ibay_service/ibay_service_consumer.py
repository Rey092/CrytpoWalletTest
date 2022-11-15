# -*- coding: utf-8 -*-
import asyncio
import json
from threading import Thread

from aio_pika import connect_robust
from aio_pika.abc import AbstractIncomingMessage, ExchangeType

from ibay_service.apps.order.dependencies import get_ibay_manager
from ibay_service.config.db import SessionLocal
from ibay_service.config.settings import settings


async def handle_new_order(message: AbstractIncomingMessage) -> None:
    db = SessionLocal()
    ibay_manager = await get_ibay_manager()
    async with message.process():
        print("========== Get new order ==========")
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

        print("========== [*] Waiting for messages from API service ==========")
        await asyncio.Future()


ibay_consumer_thread = Thread(target=asyncio.run, args=(consumer(),))
