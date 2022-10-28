# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List, Type

from sqlalchemy import desc
from sqlalchemy.orm import Session

from apps.crypto.enums import AssetCode, TransactionFee
from apps.crypto.models import Asset, Transaction, Wallet
from apps.crypto.schemas import WalletCreate


class BaseCryptoDatabase(ABC):
    """
    Crypto database adapter for SQLAlchemy ORM.
    """

    def __init__(self, wallet_model: Type[Wallet], asset_model: Type[Asset], transaction_model: Type[Transaction]):
        self.wallet = wallet_model
        self.asset = asset_model
        self.transaction = transaction_model

    @abstractmethod
    async def create_wallet(self, db: Session, wallet_create: WalletCreate) -> Wallet:
        pass

    @abstractmethod
    async def get_wallet_by_private_key(self, db: Session, private_key: str, user_id: str) -> Wallet:
        pass

    @abstractmethod
    async def get_wallet_by_address(self, db: Session, address: str) -> Wallet:
        pass

    @abstractmethod
    async def get_wallets(self, db: Session, user_id: str) -> List[Wallet]:
        pass

    @abstractmethod
    async def create_transaction(self, db: Session, transactions: List[dict]) -> None:
        pass

    @abstractmethod
    async def get_transactions(self, db: Session, address: str) -> List[Transaction]:
        pass


class EthereumDatabase(BaseCryptoDatabase):
    async def create_wallet(self, db: Session, wallet_create: WalletCreate) -> Wallet:
        asset_id = db.query(self.asset).filter(self.asset.code == AssetCode.ETH).first().id
        db_wallet = self.wallet(
            user_id=wallet_create.user_id,
            private_key=wallet_create.private_key,
            address=wallet_create.address,
            balance=wallet_create.balance,
            asset_id=asset_id,
        )
        db.add(db_wallet)
        db.commit()
        db.refresh(db_wallet)
        return db_wallet

    async def get_wallet_by_private_key(self, db: Session, private_key: str, user_id: str) -> Wallet:
        return (
            db.query(self.wallet)
            .filter(
                self.wallet.private_key == private_key,
                self.wallet.user_id == user_id,
            )
            .first()
        )

    async def get_wallet_by_address(self, db: Session, address: str) -> Wallet:
        return db.query(self.wallet).filter(self.wallet.address == address).first()

    async def get_wallets(self, db: Session, user_id: str) -> List[Wallet]:
        return db.query(self.wallet).filter(self.wallet.user_id == user_id).all()

    async def create_transaction(self, db: Session, transactions: List[dict]) -> None:
        asset_id = db.query(self.asset).filter(self.asset.code == AssetCode.ETH).first().id
        for txn in transactions:
            db_transaction = self.transaction(
                txn_hash=txn.get("txn_hash"),
                block_number=txn.get("block_number"),
                address_from=txn.get("address_from"),
                address_to=txn.get("address_to"),
                value=txn.get("value"),
                age=txn.get("age"),
                txn_fee=txn.get("txn_fee"),
                status=txn.get("status"),
                fee=TransactionFee.CRYPTOCURRENCY,
                asset_id=asset_id,
            )
            db.add(db_transaction)
            try:
                db.commit()
            except Exception:
                db.rollback()

    async def get_transactions(self, db: Session, address: str) -> List[Transaction]:
        transactions = (
            db.query(self.transaction)
            .order_by(desc(self.transaction.block_number))
            .filter(
                (self.transaction.address_from == address.lower()) | (self.transaction.address_to == address.lower()),
            )
            .all()
        )
        return transactions
