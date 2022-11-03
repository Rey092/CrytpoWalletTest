# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List, Tuple, Type

from sqlalchemy import desc
from sqlalchemy.orm import Session

from apps.crypto.enums import AssetCode, TransactionFee
from apps.crypto.models import Asset, Transaction, Wallet
from apps.crypto.schemas import WalletCreate
from apps.crypto.utils.format_date import format_date


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
    async def update_wallet_balance(self, db: Session, wallet: Wallet, value: float):
        pass

    @abstractmethod
    async def update_wallet_balance_by_transaction(self, db: Session, couples: List[Tuple[Wallet, dict]]):
        pass

    @abstractmethod
    async def get_wallets(self, db: Session) -> List[Wallet]:
        pass

    @abstractmethod
    async def get_wallet_by_private_key(self, db: Session, private_key: str, user_id: str) -> Wallet:
        pass

    @abstractmethod
    async def get_wallet_by_address(self, db: Session, address: str) -> Wallet:
        pass

    @abstractmethod
    async def get_wallets_by_user_id(self, db: Session, user_id: str) -> List[Wallet]:
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

    async def get_wallets(self, db: Session) -> List[Wallet]:
        return db.query(self.wallet).all()

    async def update_wallet_balance(self, db: Session, wallet: Wallet, value: float):
        wallet.balance = wallet.balance - value
        db.add(wallet)
        db.commit()
        db.refresh(wallet)

    async def update_wallet_balance_by_transaction(self, db: Session, couples: List[Tuple[Wallet, dict]]):
        for couple in couples:
            print(f"до {couple[0].balance}")
            print(f'тран {float(couple[1]["value"])}')
            couple[0].balance = float(couple[0].balance) + float(couple[1]["value"])
            print(f"после {couple[0].balance}")
            db.add(couple[0])
            db.commit()
            db.refresh(couple[0])

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

    async def get_wallets_by_user_id(self, db: Session, user_id: str) -> List[Wallet]:
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
                db.refresh(db_transaction)
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
        transactions = [format_date(transaction) for transaction in transactions]
        print(transactions[0].age)
        return transactions
