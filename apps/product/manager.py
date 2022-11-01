# -*- coding: utf-8 -*-
from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from apps.crypto.schemas import TransactionCreate
from apps.product.database import ProductDatabase
from apps.product.exceptions import (
    InvalidBalanceException,
    InvalidPriceException,
    InvalidProductException,
    InvalidWalletException,
)
from apps.product.models import Order, Product
from apps.product.schemas import OrderCreate, ProductCreate
from apps.users.models import User
from config.web3_clients import EthereumProviderClient


class ProductManager:
    def __init__(
        self,
        database: ProductDatabase,
        ethereum_provider: EthereumProviderClient,
    ):
        self.product_db = database
        self.ethereum_provider = ethereum_provider

    async def create_new_product(self, db: Session, product_create: ProductCreate) -> Product:
        if product_create.price <= 0:
            raise InvalidPriceException()
        product = await self.product_db.create_product(db, product_create)
        if not product:
            raise InvalidWalletException()
        return product

    async def get_all_products(self, db: Session) -> List[Product]:
        return await self.product_db.get_products(db)

    async def create_new_order(self, db: Session, order_create: OrderCreate, user: User) -> Order:
        product = await self.product_db.get_product(db, order_create.product_id)
        if not product or product.is_sold:
            raise InvalidProductException()
        try:
            wallet = [wallet for wallet in user.wallets if wallet.id == order_create.wallet_id][0]
            if wallet.balance < product.price:
                raise InvalidBalanceException()
        except IndexError:
            raise InvalidWalletException()

        transaction_create = TransactionCreate(
            address_from=wallet.address,
            address_to=product.wallet.address,
            value=product.price,
        )
        txn_hash = await self.ethereum_provider.send_raw_transaction(transaction_create, wallet)

        await self.product_db.update_is_sold_product_status(db, product.id)
        return await self.product_db.create_order(db, txn_hash, str(product.id))

    async def get_users_orders(self, db: Session, user_id: UUID) -> List[Order]:
        return await self.product_db.get_orders(db, user_id)
