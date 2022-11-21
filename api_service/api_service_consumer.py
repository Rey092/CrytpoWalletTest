# -*- coding: utf-8 -*-
import asyncio
import json
import logging
from threading import Thread

from aio_pika import connect_robust
from aio_pika.abc import AbstractIncomingMessage, ExchangeType

from api_service.apps.crypto.dependencies import get_ethereum_manager
from api_service.apps.product.dependencies import get_product_manager
from api_service.apps.users.dependencies import get_user_manager
from api_service.config.db import SessionLocal
from api_service.config.settings import settings

logger = logging.getLogger(__name__)


async def handle_new_block(message: AbstractIncomingMessage) -> None:
    db = SessionLocal()
    ethereum_manager = await get_ethereum_manager()
    async with message.process():
        logger.info(f"Got new block: {message.body}")
        await ethereum_manager.check_transactions_in_block(db, message.body.decode())


async def handle_order_to_delivery(message: AbstractIncomingMessage) -> None:
    db = SessionLocal()
    product_manager = await get_product_manager()
    async with message.process():
        logger.info("Order to delivery")
        await product_manager.update_order_by_id(db, json.loads(message.body.decode("utf-8")))


async def handle_order_failed(message: AbstractIncomingMessage) -> None:
    db = SessionLocal()
    product_manager = await get_product_manager()
    async with message.process():
        logger.info("Order failed")
        await product_manager.handle_order_failed(db, json.loads(message.body.decode("utf-8")))


async def handle_complete_order(message: AbstractIncomingMessage) -> None:
    db = SessionLocal()
    product_manager = await get_product_manager()
    async with message.process():
        logger.info("Order complete")
        await product_manager.update_order_by_id(db, json.loads(message.body.decode("utf-8")))


async def handle_count_messages(message: AbstractIncomingMessage) -> None:
    db = SessionLocal()
    user_manager = await get_user_manager()
    async with message.process():
        logger.info("Count messages")
        await user_manager.update_count_message(db, json.loads(message.body.decode("utf-8")))


async def consumer() -> None:
    connection = await connect_robust(settings.rabbit_url)
    async with connection:
        channel = await connection.channel()

        # Declaring exchanges
        new_blocks_exchange = await channel.declare_exchange(
            "new_blocks",
            ExchangeType.FANOUT,
        )
        order_to_delivery_exchange = await channel.declare_exchange(
            "order_to_delivery_exchange",
            ExchangeType.FANOUT,
        )
        order_failed_exchange = await channel.declare_exchange(
            "order_failed_exchange",
            ExchangeType.FANOUT,
        )
        order_complete_exchange = await channel.declare_exchange(
            "order_complete_exchange",
            ExchangeType.FANOUT,
        )

        count_messages_exchange = await channel.declare_exchange(
            "count_messages_exchange",
            ExchangeType.FANOUT,
        )

        # Declaring queue
        new_blocks_queue = await channel.declare_queue(exclusive=True)
        order_to_delivery_queue = await channel.declare_queue(exclusive=True)
        order_failed_queue = await channel.declare_queue(exclusive=True)
        order_complete_queue = await channel.declare_queue(exclusive=True)
        count_messages_queue = await channel.declare_queue(exclusive=True)

        # Binding the queue to the exchange
        await new_blocks_queue.bind(new_blocks_exchange)
        await order_to_delivery_queue.bind(order_to_delivery_exchange)
        await order_failed_queue.bind(order_failed_exchange)
        await order_complete_queue.bind(order_complete_exchange)
        await count_messages_queue.bind(count_messages_exchange)

        # Start listening the queue
        await new_blocks_queue.consume(handle_new_block)
        await order_to_delivery_queue.consume(handle_order_to_delivery)
        await order_failed_queue.consume(handle_order_failed)
        await order_complete_queue.consume(handle_complete_order)
        await count_messages_queue.consume(handle_count_messages)

        # Count messages for user

        logger.info("[*] Waiting for messages from services")
        await asyncio.Future()


api_consumer_thread = Thread(target=asyncio.run, args=(consumer(),))
