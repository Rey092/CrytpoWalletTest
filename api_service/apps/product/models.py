# -*- coding: utf-8 -*-
import uuid

from sqlalchemy import Boolean, Column, DateTime, Enum, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from api_service.apps.product.enums import OrderStatus
from api_service.config.db import Base


class Product(Base):
    __tablename__ = "product"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    image = Column(String)
    price = Column(Float, default=0)
    is_sold = Column(Boolean, default=False)
    date_created = Column(DateTime)
    wallet_id = Column(UUID(as_uuid=True), ForeignKey("wallet.id"))

    order = relationship("Order", backref="product", uselist=False)


class Order(Base):
    __tablename__ = "order"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    txn_hash = Column(String)
    date = Column(DateTime)
    status = Column(Enum(OrderStatus), default=OrderStatus.NEW)
    txn_hash_return = Column(String, nullable=True)
    buyer_address = Column(String)
    product_id = Column(UUID(as_uuid=True), ForeignKey("product.id"))
