# -*- coding: utf-8 -*-
from typing import Type

from sqlalchemy.orm import Session

from ibay_service.apps.order.models import OrderIBay


class OrderDatabase:
    """
    Order database(of IBay service) adapter for SQLAlchemy ORM.
    """

    def __init__(
        self,
        order_model: Type[OrderIBay],
    ):
        self.order_model = order_model

    async def create_order(self, db: Session, order_create: dict) -> None:
        db_order = self.order_model(
            order=order_create["id"],
            status=order_create["status"],
            date=order_create["date"],
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
