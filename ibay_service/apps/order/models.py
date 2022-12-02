# -*- coding: utf-8 -*-
import uuid

from sqlalchemy import Column, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID

from ibay_service.apps.order.enums import OrderStatus
from ibay_service.config.db import Base


class OrderIBay(Base):
    __tablename__ = "order_ibay"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order = Column(UUID(as_uuid=True))
    status = Column(Enum(OrderStatus))
    date = Column(DateTime)
