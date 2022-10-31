# -*- coding: utf-8 -*-
from typing import List, Type, Union

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from apps.crypto.models import Wallet
from apps.product.models import Order, Product
from apps.product.schemas import ProductCreate


class ProductDatabase:
    """
    Product database adapter for SQLAlchemy ORM.
    """

    def __init__(
        self,
        product_model: Type[Product],
        order_model: Type[Order],
        wallet_model: Type[Wallet],
    ):
        self.product = product_model
        self.order = order_model
        self.wallet = wallet_model

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
