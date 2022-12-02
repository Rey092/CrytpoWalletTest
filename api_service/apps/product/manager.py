# -*- coding: utf-8 -*-
import datetime
from typing import List

from sqlalchemy.orm import Session

from api_service.api_service_producer import ApiServiceProducer
from api_service.apps.crypto.models import Wallet
from api_service.apps.crypto.schemas import TransactionCreate
from api_service.apps.crypto.web3_clients import EthereumProviderClient
from api_service.apps.product.database import ProductDatabase
from api_service.apps.product.exceptions import (
    InvalidBalanceException,
    InvalidPriceException,
    InvalidProductException,
    InvalidWalletException,
)
from api_service.apps.product.models import Order, Product
from api_service.apps.product.schemas import OrderCreate, ProductCreate
from api_service.apps.users.models import User
from api_service.config.storage import SqlAlchemyStorage


class ProductManager:
    def __init__(
        self,
        database: ProductDatabase,
        ethereum_provider: EthereumProviderClient,
        storage: SqlAlchemyStorage,
        api_service_producer: ApiServiceProducer,
    ):
        self.product_db = database
        self.ethereum_provider = ethereum_provider
        self.storage = storage
        self.api_service_producer = api_service_producer

    async def create_new_product(self, db: Session, product_create: ProductCreate) -> Product:
        if product_create.price <= 0:
            raise InvalidPriceException()
        product_create.image = await self.storage.upload(
            file=product_create.image,
            upload_to="ibay",
            sizes=(150, 150),
            content_types=["png", "jpg", "jpeg"],
        )
        product = await self.product_db.create_product(db, product_create)
        if not product:
            raise InvalidWalletException()
        message = {
            "id": str(product.id),
            "image": product.image,
            "title": product.title,
            "price": product.price,
            "wallet": {
                "address": product.wallet.address,
            },
        }
        await self.api_service_producer.publish_message(
            exchange_name="new_product_exchange",
            message=message,
        )
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

        await self.product_db.update_wallet_balance(db, wallet, product.price)
        transaction_create = TransactionCreate(
            address_from=wallet.address,
            address_to=product.wallet.address,
            value=product.price,
        )
        txn_hash = await self.ethereum_provider.send_raw_transaction(transaction_create, wallet)

        await self.product_db.update_is_sold_product_status(db, product.id)
        order = await self.product_db.create_order(db, txn_hash, str(product.id), wallet.address)
        message = {
            "id": str(order.id),
            "product": {
                "id": str(order.product.id),
                "image": order.product.image,
                "title": order.product.title,
                "price": order.product.price,
            },
            "txnHash": order.txn_hash,
            "date": datetime.datetime.strptime(str(order.date), "%d.%m.%Y %H:%M").strftime("%d.%m.%Y %H:%M"),
            "status": "NEW",
            "buyerAddress": order.buyer_address,
            "txnHashReturn": None,
        }
        await self.api_service_producer.publish_message(
            exchange_name="new_order_exchange",
            message=message,
        )
        return order

    async def get_users_orders(self, db: Session, wallets: List[Wallet]) -> List[Order]:
        addresses = [wallet.address for wallet in wallets]
        return await self.product_db.get_orders(db, addresses)

    async def update_order_by_id(self, db: Session, order: dict) -> Order:
        return await self.product_db.update_order_by_id(db, order)

    async def handle_order_failed(self, db: Session, order: dict):
        updated_order = await self.update_order_by_id(db, order)
        order_txn = await self.product_db.get_transaction(db, updated_order.txn_hash)
        updated_value = order_txn.value - (order_txn.txn_fee * 1.5)

        transaction_create = TransactionCreate(
            address_from=updated_order.product.wallet.address,
            address_to=updated_order.buyer_address,
            value=updated_value,
        )
        txn_hash = await self.ethereum_provider.send_raw_transaction(transaction_create, updated_order.product.wallet)
        await self.product_db.update_wallet_balance(db, updated_order.product.wallet, updated_value)

        updated_order.status = "RETURN"
        updated_order.txn_hash_return = txn_hash
        await self.product_db.update_order(db, updated_order)

        order_return_message = {
            "order": str(updated_order.id),
            "status": "RETURN",
            "txnHashReturn": txn_hash,
        }
        await self.api_service_producer.publish_message(
            exchange_name="order_return_exchange",
            message=order_return_message,
        )

        txn_return_message = {
            "address_from": updated_order.product.wallet.address,
            "value": updated_value,
            "txn_hash": txn_hash,
        }
        await self.api_service_producer.publish_message(
            exchange_name="txn_return_exchange",
            message=txn_return_message,
        )
