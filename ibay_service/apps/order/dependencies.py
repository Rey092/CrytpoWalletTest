# -*- coding: utf-8 -*-
from async_lru import alru_cache

from ibay_service.apps.order.database import OrderDatabase
from ibay_service.apps.order.manager import IBayManager
from ibay_service.apps.order.models import OrderIBay
from ibay_service.ibay_service_producer import Producer


@alru_cache()
async def get_order_db() -> OrderDatabase:
    return OrderDatabase(OrderIBay)


@alru_cache()
async def get_ibay_service_producer() -> Producer:
    return Producer()


@alru_cache()
async def get_ibay_manager() -> IBayManager:
    order_db = await get_order_db()
    producer = await get_ibay_service_producer()
    return IBayManager(order_db, producer)
