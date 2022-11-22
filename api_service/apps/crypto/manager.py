# -*- coding: utf-8 -*-
import secrets
from abc import abstractmethod
from typing import List

from aioredis import Redis
from eth_account import Account
from sqlalchemy.orm import Session

from api_service.api_service_producer import ApiServiceProducer
from api_service.apps.crypto.web3_clients import EthereumProviderClient, EtherscanClient

from .database import BaseCryptoDatabase
from .exceptions import (
    InvalidPrivateKeyException,
    InvalidSenderException,
    InvalidValueException,
    WalletAlreadyExistException,
)
from .models import Transaction, Wallet
from .schemas import TransactionCreate, WalletCreate


class BaseCryptoManager:
    def __init__(
        self,
        database: BaseCryptoDatabase,
        etherscan_client: EtherscanClient,
        ethereum_provider: EthereumProviderClient,
        api_service_producer: ApiServiceProducer,
        redis: Redis,
    ):
        self.ethereum_db = database
        self.etherscan_client = etherscan_client
        self.ethereum_provider = ethereum_provider
        self.api_service_producer = api_service_producer
        self.redis = redis

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
        generated_wallet.balance = await self.parse_wallet_balance(generated_wallet.address)
        created_wallet = await self.ethereum_db.create_wallet(db, generated_wallet)
        transactions = await self.etherscan_client.get_list_transactions(created_wallet.address)
        if transactions:
            await self.ethereum_db.create_transaction(db, transactions)
        return created_wallet

    async def get_all_users_wallets(self, db: Session, user_id: str) -> List[Wallet]:
        return await self.ethereum_db.get_wallets_by_user_id(db, user_id)

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
        txn_hash = await self.ethereum_provider.send_raw_transaction(transaction_create, wallet_from)
        if txn_hash:
            await self.ethereum_db.update_wallet_balance(db, wallet_from, transaction_create.value)
        return {"txn_hash": txn_hash}

    async def check_transactions_in_block(self, db: Session, block_hash: str):
        wallets = await self.get_all_wallets(db)
        addresses = [wallet.address for wallet in wallets]
        checked_transactions = await self.ethereum_provider.get_transactions_from_block(block_hash, addresses)
        if checked_transactions:
            delete_cache_list = [txn["to"] for txn in checked_transactions if txn["to"] in addresses]
            [delete_cache_list.append(txn["from"]) for txn in checked_transactions if txn["from"] in addresses]
            await self.clear_cache(delete_cache_list)
            transactions = await self.etherscan_client.get_result({"result": checked_transactions})
            await self.ethereum_db.create_transaction(db, transactions)
            couples_for_update_balance = [
                (wallet, transaction)
                for wallet in wallets
                for transaction in transactions
                if wallet.address.lower() == transaction["address_to"].lower()
            ]
            message = [
                {
                    "address_to": couple[1]["address_to"],
                    "txn_hash": couple[1]["txn_hash"],
                    "value": couple[1]["value"],
                    "new_balance": couple[0].balance + float(couple[1]["value"]),
                }
                for couple in couples_for_update_balance
            ]
            await self.api_service_producer.publish_message(
                exchange_name="new_transactions_exchange",
                message=message,
            )
            await self.ethereum_db.update_wallet_balance_by_transaction(db, couples_for_update_balance)

    async def get_all_wallets(self, db: Session) -> List[Wallet]:
        return await self.ethereum_db.get_wallets(db)

    async def parse_wallet_balance(self, address: str):
        return await self.ethereum_provider.get_balance(address)

    async def update_wallets_balances(self, db: Session, wallets: List[Wallet]):
        await self.ethereum_db.update_balances(db, wallets)

    async def clear_cache(self, addresses):
        for address in addresses:
            cursor, keys = await self.redis.scan(match=f"fastapi-cache:wallet-history:{address}:*")
            for key in keys:
                await self.redis.delete(key)
