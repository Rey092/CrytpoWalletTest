# -*- coding: utf-8 -*-
import uuid

from sqlalchemy import BigInteger, Boolean, Column, Enum, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from apps.crypto.enums import AssetCode, AssetNetwork, AssetStandard, AssetType
from config.db import Base


class Asset(Base):
    __tablename__ = "asset"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(Enum(AssetCode))
    network = Column(Enum(AssetNetwork))
    type = Column(Enum(AssetType))
    standard = Column(Enum(AssetStandard), nullable=True)
    decimals = Column(BigInteger)
    is_currency = Column(Boolean)

    wallets = relationship("Wallet", back_populates="asset")


class Wallet(Base):
    __tablename__ = "wallet"

    wallet_address = Column(String, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    user = relationship("User", back_populates="wallets")
    private_key = Column(String)
    balance = Column(Float, default=0)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("asset.id"))
    asset = relationship("Asset", back_populates="wallets")
