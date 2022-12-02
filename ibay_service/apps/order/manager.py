# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session

from ibay_service.apps.order.database import OrderDatabase
from ibay_service.apps.order.models import OrderIBay
from ibay_service.config.utils.send_10000_requests import send_requests
from ibay_service.ibay_service_producer import Producer


class IBayManager:
    def __init__(
        self,
        database: OrderDatabase,
        producer: Producer,
    ):
        self.order_db = database
        self.producer = producer

    async def create_new_order(self, db: Session, order_create: dict) -> None:
        order = await self.order_db.create_order(db, order_create)
        if await send_requests():
            order.status = "DELIVERY"
            message = {
                "order": str(order.order),
                "status": "DELIVERY",
            }
            await self.producer.publish_message(
                exchange_name="order_to_delivery_exchange",
                message=message,
            )
        else:
            order.status = "FAILED"
            message = {
                "order": str(order.order),
                "status": "FAILED",
            }
            await self.producer.publish_message(
                exchange_name="order_failed_exchange",
                message=message,
            )
        await self.update_order(db, order)

    async def update_order(self, db: Session, order: OrderIBay):
        await self.order_db.update_order(db, order)

    async def handle_returned_order(self, db: Session, returned_order: dict) -> None:
        await self.order_db.update_returned_order(db, returned_order)
