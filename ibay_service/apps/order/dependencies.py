# -*- coding: utf-8 -*-
from async_lru import alru_cache

from ibay_service.apps.order.database import OrderDatabase
from ibay_service.apps.order.manager import IBayManager
from ibay_service.apps.order.models import OrderIBay


@alru_cache()
async def get_order_db() -> OrderDatabase:
    return OrderDatabase(OrderIBay)


# @alru_cache()
# async def get_ibay_service_producer() -> ApiServiceProducer:
#     return ApiServiceProducer()


@alru_cache()
async def get_ibay_manager() -> IBayManager:
    order_db = await get_order_db()
    # api_service_producer = await get_api_service_producer()
    return IBayManager(order_db)
