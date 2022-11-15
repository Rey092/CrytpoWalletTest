# -*- coding: utf-8 -*-
import datetime
from typing import List, Type, Union
from uuid import UUID

from sqlalchemy import asc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api_service.apps.crypto.models import Wallet
from api_service.apps.product.models import Order, Product
from api_service.apps.product.schemas import ProductCreate
from api_service.apps.product.utils.format_date import format_date
from api_service.apps.users.models import User


class ProductDatabase:
    """
    Product database adapter for SQLAlchemy ORM.
    """

    def __init__(
        self,
        product_model: Type[Product],
        order_model: Type[Order],
        wallet_model: Type[Wallet],
        user_model: Type[User],
    ):
        self.product = product_model
        self.order = order_model
        self.wallet = wallet_model
        self.user = user_model

    async def create_product(self, db: Session, product_create: ProductCreate) -> Union[Product, None]:
        db_product = self.product(
            wallet_id=product_create.wallet_id,
            title=product_create.title,
            image=product_create.image,
            price=product_create.price,
            date_created=datetime.datetime.now(),
        )
        db.add(db_product)
        try:
            db.commit()
            db.refresh(db_product)
        except IntegrityError:
            return None
        return db_product

    async def get_products(self, db: Session) -> List[Product]:
        return (
            db.query(self.product)
            .order_by(asc(self.product.date_created))
            .filter(self.product.is_sold == False)  # noqa
            .all()
        )

    async def get_product(self, db: Session, product_id: UUID) -> Product:
        return db.query(self.product).filter(self.product.id == product_id).first()

    async def update_is_sold_product_status(self, db: Session, product_id: UUID) -> None:
        product = db.query(self.product).get(product_id)
        product.is_sold = True
        db.add(product)
        db.commit()
        db.refresh(product)

    async def create_order(self, db: Session, txn_hash: str, product_id: str, buyer_address: str) -> Order:
        db_order = self.order(
            txn_hash=txn_hash,
            product_id=product_id,
            buyer_address=buyer_address,
            date=datetime.datetime.now(),
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return format_date(db_order)

    async def update_wallet_balance(self, db: Session, wallet: Wallet, value: float):
        wallet = db.query(self.wallet).filter(self.wallet.id == wallet.id).first()
        wallet.balance -= value
        db.add(wallet)
        db.commit()
        db.refresh(wallet)

    async def get_orders(self, db: Session, addresses: List[str]) -> List[Order]:
        orders = db.query(self.order).order_by(asc(self.order.date)).filter(self.order.buyer_address.in_(addresses))
        orders = [format_date(order) for order in orders]
        return orders
