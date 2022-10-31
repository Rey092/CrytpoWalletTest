# -*- coding: utf-8 -*-
from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from apps.product.database import ProductDatabase
from apps.product.exceptions import InvalidPriceException, InvalidWalletException
from apps.product.schemas import ProductCreate, ProductCreateResponse, ProductDetail


class ProductManager:
    def __init__(
        self,
        database: ProductDatabase,
    ):
        self.product_db = database

    async def create_new_product(self, db: Session, product_create: ProductCreate) -> ProductCreateResponse:
        if product_create.price <= 0:
            raise InvalidPriceException()
        product = await self.product_db.create_product(db, product_create)
        if not product:
            raise InvalidWalletException()
        return ProductCreateResponse(**jsonable_encoder(product), address=product.wallet.address)

    async def get_all_products(self, db: Session) -> List[ProductDetail]:
        products = await self.product_db.get_products(db)
        products_data = [
            ProductDetail(**jsonable_encoder(product), address=product.wallet.address) for product in products
        ]
        return products_data
