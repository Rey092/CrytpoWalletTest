# -*- coding: utf-8 -*-
import uuid

from sqlalchemy import Boolean, Column, DateTime, Enum, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from apps.product.enums import OrderStatus
from config.db import Base


class Product(Base):
    __tablename__ = "product"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    image = Column(String)
    price = Column(Float, default=0)
    is_sold = Column(Boolean, default=False)
    wallet_id = Column(UUID(as_uuid=True), ForeignKey("wallet.id"))

    order = relationship("Order", backref="product", uselist=False)


class Order(Base):
    __tablename__ = "order"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    has_access_chat = Column(Boolean, default=True)
    txn_hash = Column(String)
    date = Column(DateTime)
    status = Column(Enum(OrderStatus), default=OrderStatus.NEW)
    txn_hash_return = Column(String)
    product_id = Column(UUID(as_uuid=True), ForeignKey("product.id"))
