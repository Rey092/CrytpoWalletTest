# -*- coding: utf-8 -*-
import asyncio
import random
from threading import Thread
from typing import Optional

from sqlalchemy.orm import Session

from ibay_service.apps.order.database import OrderDatabase
from ibay_service.apps.order.models import OrderIBay
from ibay_service.config.db import SessionLocal
from ibay_service.ibay_service_producer import Producer


class OrderHandler:
    def __init__(
        self,
        order_db: OrderDatabase,
        producer: Producer,
    ) -> None:
        self.order_db = order_db
        self.producer = producer

    async def get_order_with_delivery_status(self, db: Session) -> Optional[OrderIBay]:
        return await self.order_db.get_delivery_order(db)

    async def complete_or_failed_order(self):
        print("======== Order Handler is active ========")

        chance = [True, False]

        while True:
            await asyncio.sleep(5)
            db = SessionLocal()
            order = await self.get_order_with_delivery_status(db)

            if order:
                if random.choice(chance):
                    order.status = "COMPLETE"
                    message = {
                        "order": str(order.order),
                        "status": "COMPLETE",
                    }
                    await self.producer.publish_message(
                        exchange_name="order_complete_exchange",
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
                await self.order_db.update_order(db, order)


order_handler = OrderHandler(OrderDatabase(OrderIBay), Producer())

order_handler_thread = Thread(target=asyncio.run, args=(order_handler.complete_or_failed_order(),))
