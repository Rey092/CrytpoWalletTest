# -*- coding: utf-8 -*-
import json
from typing import Union

import aio_pika
from aio_pika import DeliveryMode, ExchangeType, Message

from config.settings import settings


class ApiServiceProducer:
    async def publish_message(
        self,
        exchange_name: str,
        message: Union[str, list, dict],
        exchange_type: Union[ExchangeType, None] = ExchangeType.FANOUT,
        delivery_mode: Union[DeliveryMode, int, None] = DeliveryMode.PERSISTENT,
    ):
        connection = await aio_pika.connect_robust(settings.rabbit_url)

        async with connection:
            channel = await connection.channel()
            exchange = await self.create_exchange(channel, exchange_name, exchange_type)
            message = await self.create_message(message, delivery_mode)
            await exchange.publish(message, routing_key="info")

    @staticmethod
    async def create_exchange(channel, exchange_name, exchange_type):
        exchange = await channel.declare_exchange(
            exchange_name,
            exchange_type,
        )
        return exchange

    @staticmethod
    async def create_message(message, delivery_mode):
        message = Message(
            json.dumps(message).encode(),
            delivery_mode=delivery_mode,
        )
        return message
