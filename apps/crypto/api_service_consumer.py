# -*- coding: utf-8 -*-
import asyncio
import logging
from threading import Thread

from aio_pika import connect_robust
from aio_pika.abc import AbstractIncomingMessage, ExchangeType

from apps.crypto.dependencies import get_ethereum_manager
from config.db import SessionLocal
from config.settings import settings

logger = logging.getLogger(__name__)


async def on_message(message: AbstractIncomingMessage) -> None:
    db = SessionLocal()
    ethereum_manager = await get_ethereum_manager()
    async with message.process():
        logger.info(f"Got new block: {message.body}")

        await ethereum_manager.check_transactions_in_block(db, message.body.decode())


async def consumer() -> None:
    connection = await connect_robust(settings.rabbit_url)
    async with connection:
        channel = await connection.channel()

        new_blocks_exchange = await channel.declare_exchange(
            "new_blocks",
            ExchangeType.FANOUT,
        )

        # Declaring queue
        queue = await channel.declare_queue(exclusive=True)

        # Binding the queue to the exchange
        await queue.bind(new_blocks_exchange)

        # Start listening the queue
        await queue.consume(on_message)

        logger.info("[*] Waiting for messages form ethereum service")
        await asyncio.Future()


main_consumer_thread = Thread(target=asyncio.run, args=(consumer(),))
