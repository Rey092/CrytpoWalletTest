# -*- coding: utf-8 -*-
from typing import Optional, Type

from sqlalchemy import asc
from sqlalchemy.orm import Session

from ibay_service.apps.order.enums import OrderStatus
from ibay_service.apps.order.models import OrderIBay


class OrderDatabase:
    """
    Order database(of IBay service) adapter for SQLAlchemy ORM.
    """

    def __init__(
        self,
        order_model: Type[OrderIBay],
    ):
        self.order = order_model

    async def create_order(self, db: Session, order_create: dict) -> OrderIBay:
        db_order = self.order(
            order=order_create["id"],
            status=order_create["status"],
            date=order_create["date"],
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order

    @staticmethod
    async def update_order(db: Session, order: OrderIBay) -> None:
        db.add(order)
        db.commit()
        db.refresh(order)

    async def update_returned_order(self, db: Session, returned_order: dict) -> None:
        order = db.query(self.order).filter(self.order.order == returned_order["order"]).first()
        order.status = "RETURN"
        db.add(order)
        db.commit()
        db.refresh(order)

    async def get_delivery_order(self, db: Session) -> Optional[OrderIBay]:
        return (
            db.query(self.order)
            .order_by(asc(self.order.date))
            .filter(self.order.status == OrderStatus.DELIVERY)
            .first()
        )
