# -*- coding: utf-8 -*-
import uuid

from sqlalchemy import Column, DateTime, Enum, String
from sqlalchemy.dialects.postgresql import UUID

from apps.ibay.config.db import BaseIBay
from apps.ibay.enums import OrderStatus


class OrderIBay(BaseIBay):
    __tablename__ = "order_ibay"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order = Column(UUID(as_uuid=True))
    status = Column(Enum(OrderStatus))
    txn_hash_return = Column(String, nullable=True)
    date = Column(DateTime)
