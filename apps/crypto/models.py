# -*- coding: utf-8 -*-
import uuid

from sqlalchemy import BigInteger, Boolean, Column, Enum, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from apps.crypto.enums import AssetCode, AssetNetwork, AssetStandard, AssetType, TransactionFee
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

    wallets = relationship("Wallet", backref="asset")
    transactions = relationship("Transaction", backref="asset")


class Wallet(Base):
    __tablename__ = "wallet"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    private_key = Column(String)
    address = Column(String)
    balance = Column(Float, default=0)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("asset.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))

    products = relationship("Product", backref="wallet")

    __table_args__ = (UniqueConstraint("user_id", "private_key"),)


class Transaction(Base):
    __tablename__ = "transaction"

    txn_hash = Column(String, primary_key=True)
    block_number = Column(Integer)
    address_from = Column(String)
    address_to = Column(String)
    value = Column(Float)
    age = Column(Integer)
    txn_fee = Column(Float)
    status = Column(Boolean)
    fee = Column(Enum(TransactionFee))
    asset_id = Column(UUID(as_uuid=True), ForeignKey("asset.id"))
