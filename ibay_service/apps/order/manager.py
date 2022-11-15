# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session

from ibay_service.apps.order.database import OrderDatabase


class IBayManager:
    def __init__(
        self,
        database: OrderDatabase,
    ):
        self.order_db = database

    async def create_new_order(self, db: Session, order_create: dict) -> None:
        await self.order_db.create_order(db, order_create)
