# -*- coding: utf-8 -*-
import uuid

from sqlalchemy import Column, Enum, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from config.db import Base


class Asset(Base):
    __tablename__ = "asset"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset = Column(Enum("ethereum_token", name="asset_enum"))

    wallets = relationship("Wallet", back_populates="asset")


class Wallet(Base):
    __tablename__ = "wallet"

    wallet_number = Column(String, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    user = relationship("User", back_populates="wallets")
    private_key = Column(String)
    address = Column(String)
    balance = Column(Float)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("asset.id"))
    asset = relationship("Asset", back_populates="wallets")
    network = Column(Enum("ethereum", name="network_enum"))
