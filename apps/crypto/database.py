# -*- coding: utf-8 -*-
"""
FastAPI Crypto database adapter for SQLAlchemy ORM.
"""
from abc import ABC, abstractmethod
from typing import Type

from sqlalchemy.orm import Session

from apps.crypto.enums import AssetCode
from apps.crypto.models import Asset, Wallet
from apps.crypto.schemas import WalletCreate


class BaseCryptoDatabase(ABC):
    """
    Crypto database adapter for SQLAlchemy ORM.
    """

    def __init__(self, wallet_model: Type[Wallet], asset_model: Type[Asset]):
        self.wallet = wallet_model
        self.asset = asset_model

    @abstractmethod
    async def create_wallet(self, wallet_create: WalletCreate, db: Session) -> Wallet:
        pass

    @abstractmethod
    async def get_wallet_by_private_key(self, private_key: str, db: Session) -> Wallet:
        pass


class EthereumDatabase(BaseCryptoDatabase):
    async def create_wallet(self, wallet_create: WalletCreate, db: Session) -> Wallet:
        asset_id = db.query(self.asset).filter(self.asset.code == AssetCode.ETH).first().id
        db_wallet = self.wallet(
            wallet_address=wallet_create.wallet_address,
            user_id=wallet_create.user_id,
            private_key=wallet_create.private_key,
            asset_id=asset_id,
        )
        db.add(db_wallet)
        db.commit()
        db.refresh(db_wallet)
        return db_wallet

    async def get_wallet_by_private_key(self, private_key: str, db: Session) -> Wallet:
        return db.query(self.wallet).filter(self.wallet.private_key == private_key).first()
