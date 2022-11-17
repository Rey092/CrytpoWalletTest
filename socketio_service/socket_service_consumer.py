# -*- coding: utf-8 -*-
import asyncio
import json
from threading import Thread

from aio_pika import connect_robust
from aio_pika.abc import AbstractIncomingMessage, ExchangeType

from socketio_service.apps.chat.dependencies import get_client_dispatcher
from socketio_service.config.settings import settings


async def handle_updating_wallet_balance(message: AbstractIncomingMessage) -> None:
    client = await get_client_dispatcher()
    async with message.process():
        print("========== Wallet balance updated ==========")
        await client.update_balance(json.loads(message.body.decode("utf-8")))


async def handle_new_transactions(message: AbstractIncomingMessage) -> None:
    client = await get_client_dispatcher()
    async with message.process():
        print("========== New Transactions ==========")
        await client.new_transactions(json.loads(message.body.decode("utf-8")))


async def handle_new_product(message: AbstractIncomingMessage) -> None:
    client = await get_client_dispatcher()
    async with message.process():
        print("========== New Product ==========")
        await client.new_product(json.loads(message.body.decode("utf-8")))


async def handle_new_order(message: AbstractIncomingMessage) -> None:
    client = await get_client_dispatcher()
    async with message.process():
        print("========== New Order ==========")
        await client.new_order(json.loads(message.body.decode("utf-8")))


async def handle_update_order(message: AbstractIncomingMessage) -> None:
    client = await get_client_dispatcher()
    async with message.process():
        print(f"========== Update Order {message.body.decode()} ==========")
        await client.update_order(json.loads(message.body.decode("utf-8")))


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
        # ibay
        new_product_exchange = await channel.declare_exchange(
            "new_product_exchange",
            ExchangeType.FANOUT,
        )
        new_order_exchange = await channel.declare_exchange(
            "new_order_exchange",
            ExchangeType.FANOUT,
        )
        # update orders
        order_to_delivery_exchange = await channel.declare_exchange(
            "order_to_delivery_exchange",
            ExchangeType.FANOUT,
        )
        order_failed_exchange = await channel.declare_exchange(
            "order_failed_exchange",
            ExchangeType.FANOUT,
        )
        order_return_exchange = await channel.declare_exchange(
            "order_return_exchange",
            ExchangeType.FANOUT,
        )
        order_complete_exchange = await channel.declare_exchange(
            "order_complete_exchange",
            ExchangeType.FANOUT,
        )

        # Declaring queue
        wallet_balance_queue = await channel.declare_queue(exclusive=True)
        new_transactions_queue = await channel.declare_queue(exclusive=True)
        # ibay
        new_product_queue = await channel.declare_queue(exclusive=True)
        new_order_queue = await channel.declare_queue(exclusive=True)
        # update orders
        order_to_delivery_queue = await channel.declare_queue(exclusive=True)
        order_failed_queue = await channel.declare_queue(exclusive=True)
        order_return_queue = await channel.declare_queue(exclusive=True)
        order_complete_queue = await channel.declare_queue(exclusive=True)

        # Binding the queue to the exchange
        await wallet_balance_queue.bind(wallet_balance_exchange)
        await new_transactions_queue.bind(new_transactions_exchange)
        # ibay
        await new_product_queue.bind(new_product_exchange)
        await new_order_queue.bind(new_order_exchange)
        # update orders
        await order_to_delivery_queue.bind(order_to_delivery_exchange)
        await order_failed_queue.bind(order_failed_exchange)
        await order_return_queue.bind(order_return_exchange)
        await order_complete_queue.bind(order_complete_exchange)

        # Start listening the queue
        await wallet_balance_queue.consume(handle_updating_wallet_balance)
        await new_transactions_queue.consume(handle_new_transactions)
        # ibay
        await new_product_queue.consume(handle_new_product)
        await new_order_queue.consume(handle_new_order)
        # update orders
        await order_to_delivery_queue.consume(handle_update_order)
        await order_failed_queue.consume(handle_update_order)
        await order_return_queue.consume(handle_update_order)
        await order_complete_queue.consume(handle_update_order)

        print("========== [*] Waiting for messages from services ==========")
        await asyncio.Future()


socket_consumer_thread = Thread(target=asyncio.run, args=(consumer(),))
