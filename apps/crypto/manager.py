# -*- coding: utf-8 -*-
import secrets
from abc import abstractmethod
from typing import List

from eth_account import Account
from sqlalchemy.orm import Session

from ..users.jwt_backend import JWTBackend
from .database import BaseCryptoDatabase
from .exceptions import (
    InvalidPrivateKeyException,
    InvalidSenderException,
    InvalidValueException,
    WalletAlreadyExistException,
)
from .models import Transaction, Wallet
from .schemas import TransactionCreate, WalletCreate
from .web3_clients import EtherscanClient, InfuraClient


class BaseCryptoManager:
    def __init__(
        self,
        database: BaseCryptoDatabase,
        jwt_backend: JWTBackend,
        etherscan_client: EtherscanClient,
        infura_client: InfuraClient,
    ):
        self.ethereum_db = database
        self.jwt_backend = jwt_backend
        self.etherscan_client = etherscan_client
        self.infura_client = infura_client

    async def generate_private_key(self, wallet: WalletCreate) -> WalletCreate:
        hex_string = secrets.token_hex(32)
        private_key = "0x" + hex_string
        wallet.private_key = private_key
        return await self.get_wallet_address(private_key, wallet)

    @staticmethod
    async def get_wallet_address(private_key, wallet: WalletCreate) -> WalletCreate:
        try:
            account = Account.from_key(private_key)
            wallet.address = account.address
        except Exception as ex:
            raise InvalidPrivateKeyException(message=str(ex))
        return wallet

    @abstractmethod
    async def create_new_wallet(self, db: Session, data: dict) -> Wallet:
        pass

    @abstractmethod
    async def import_existing_wallet(self, db: Session, wallet: WalletCreate) -> Wallet:
        pass


class EthereumManager(BaseCryptoManager):
    async def create_new_wallet(self, db: Session, wallet: WalletCreate) -> Wallet:
        generated_wallet = await self.generate_private_key(wallet)
        return await self.ethereum_db.create_wallet(db, generated_wallet)

    async def import_existing_wallet(self, db: Session, wallet: WalletCreate) -> Wallet:
        if await self.ethereum_db.get_wallet_by_private_key(db, wallet.private_key, wallet.user_id):
            raise WalletAlreadyExistException()
        generated_wallet = await self.get_wallet_address(wallet.private_key, wallet)
        generated_wallet.balance = await self.infura_client.get_balance(generated_wallet.address)
        created_wallet = await self.ethereum_db.create_wallet(db, generated_wallet)
        transactions = await self.etherscan_client.get_list_transactions(created_wallet.address)
        if transactions:
            await self.ethereum_db.create_transaction(db, transactions)
        return created_wallet

    async def get_all_users_wallets(self, db: Session, user_id: str) -> List[Wallet]:
        return await self.ethereum_db.get_wallets(db, user_id)

    async def get_transactions_by_wallet_address(self, db: Session, address: str) -> List[Transaction]:
        return await self.ethereum_db.get_transactions(db, address)

    async def send_transaction(self, db: Session, transaction_create: TransactionCreate) -> dict:
        if transaction_create.value < 0:
            raise InvalidValueException(message="The value cannot be less than zero.")
        wallet_from = await self.ethereum_db.get_wallet_by_address(db, transaction_create.address_from)
        if not wallet_from:
            raise InvalidSenderException()
        if (wallet_from.balance - 0.001) < transaction_create.value:
            raise InvalidValueException(message="The value exceeds the balance of the wallet.")
        txn_hash = await self.infura_client.send_raw_transaction(transaction_create, wallet_from)
        return {"txn_hash": txn_hash}

    async def check_transactions_in_block(self, db: Session, block_hash: str):
        pass
