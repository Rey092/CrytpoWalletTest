# -*- coding: utf-8 -*-
import asyncio
import json
import logging
from threading import Thread

from aio_pika import connect_robust
from aio_pika.abc import AbstractIncomingMessage, ExchangeType

from apps.socketio_app.dependencies import get_client_dispatcher
from config.settings import settings

logger = logging.getLogger(__name__)


async def handle_updating_wallet_balance(message: AbstractIncomingMessage) -> None:
    client = await get_client_dispatcher()
    async with message.process():
        logger.info(f"Wallet balance: {message.body}")
        await client.update_balance(json.loads(message.body.decode("utf-8")))


async def handle_new_transactions(message: AbstractIncomingMessage) -> None:
    client = await get_client_dispatcher()
    async with message.process():
        logger.info(f"New Transactions: {message.body}")
        await client.new_transactions(json.loads(message.body.decode("utf-8")))


async def consumer() -> None:
    connection = await connect_robust(settings.rabbit_url)
    async with connection:
        channel = await connection.channel()

        # create exchanges
        wallet_balance_exchange = await channel.declare_exchange(
            "wallet_balance_exchange",
            ExchangeType.FANOUT,
        )
        new_transactions_exchange = await channel.declare_exchange(
            "new_transactions_exchange",
            ExchangeType.FANOUT,
        )

        # Declaring queue
        wallet_balance_queue = await channel.declare_queue(exclusive=True)
        new_transactions_queue = await channel.declare_queue(exclusive=True)

        # Binding the queue to the exchange
        await wallet_balance_queue.bind(wallet_balance_exchange)
        await new_transactions_queue.bind(new_transactions_exchange)

        # Start listening the queue
        await wallet_balance_queue.consume(handle_updating_wallet_balance)
        await new_transactions_queue.consume(handle_new_transactions)

        logger.info("[*] Waiting for messages from API service")
        await asyncio.Future()


socket_consumer_thread = Thread(target=asyncio.run, args=(consumer(),))
