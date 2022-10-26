# -*- coding: utf-8 -*-
import secrets
from abc import abstractmethod

from eth_account import Account
from sqlalchemy.orm import Session

from ..users.jwt_backend import JWTBackend
from .database import BaseCryptoDatabase
from .exceptions import WalletAlreadyExistException
from .models import Wallet
from .schemas import WalletCreate


class BaseCryptoManager:
    def __init__(
        self,
        database: BaseCryptoDatabase,
        jwt_backend: JWTBackend,
    ):
        self.ethereum_db = database
        self.jwt_backend = jwt_backend

    async def generate_private_key(self, wallet: WalletCreate) -> WalletCreate:
        hex_string = secrets.token_hex(32)
        private_key = "0x" + hex_string
        wallet.private_key = private_key
        return await self.get_wallet_address(private_key, wallet)

    @staticmethod
    async def get_wallet_address(private_key, wallet: WalletCreate) -> WalletCreate:
        account = Account.from_key(private_key)
        wallet.wallet_address = account.address
        return wallet

    @abstractmethod
    async def create_new_wallet(self, db: Session, data: dict) -> Wallet:
        """

        :param db:
        :param data:
        :return:
        """

    @abstractmethod
    async def import_existing_wallet(self, db: Session, wallet: WalletCreate):
        """

        :param db:
        :param wallet:
        :return:
        """


class EthereumManager(BaseCryptoManager):
    async def create_new_wallet(self, db: Session, wallet: WalletCreate) -> Wallet:
        wallet = await self.generate_private_key(wallet)
        return await self.ethereum_db.create_wallet(wallet, db)

    async def import_existing_wallet(self, db: Session, wallet: WalletCreate) -> Wallet:
        if await self.ethereum_db.get_wallet_by_private_key(wallet.private_key, db):
            raise WalletAlreadyExistException()
        wallet = await self.get_wallet_address(wallet.private_key, wallet)
        return await self.ethereum_db.create_wallet(wallet, db)
