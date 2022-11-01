# -*- coding: utf-8 -*-
from typing import List, Type, Union
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from apps.crypto.models import Wallet
from apps.product.models import Order, Product
from apps.product.schemas import ProductCreate
from apps.product.utils.format_date import format_date
from apps.users.models import User


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
        )
        db.add(db_product)
        try:
            db.commit()
            db.refresh(db_product)
        except IntegrityError:
            return None
        return db_product

    async def get_products(self, db: Session) -> List[Product]:
        return db.query(self.product).filter(self.product.is_sold == False).all()  # noqa

    async def get_product(self, db: Session, product_id: UUID) -> Product:
        return db.query(self.product).filter(self.product.id == product_id).first()

    async def update_is_sold_product_status(self, db: Session, product_id: UUID) -> None:
        product = db.query(self.product).get(product_id)
        product.is_sold = True
        db.add(product)
        db.commit()
        db.refresh(product)

    async def create_order(self, db: Session, txn_hash: str, product_id: str) -> Order:
        db_order = self.order(
            txn_hash=txn_hash,
            product_id=product_id,
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return format_date(db_order)

    async def get_orders(self, db: Session, user_id: UUID) -> List[Order]:
        orders = (
            db.query(self.order)
            .join(self.product)
            .join(self.wallet)
            .join(self.user)
            .filter(
                self.user.id == user_id,
            )
            .all()
        )
        orders = [format_date(order) for order in orders]
        return orders
