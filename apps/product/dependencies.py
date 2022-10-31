# -*- coding: utf-8 -*-
from async_lru import alru_cache
from fastapi_helper.schemas.examples_generate import ExamplesGenerate

from apps.crypto.models import Wallet
from apps.product.database import ProductDatabase
from apps.product.manager import ProductManager
from apps.product.models import Order, Product
from config.db import SessionLocal

examples_generate = ExamplesGenerate()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@alru_cache()
async def get_product_db() -> ProductDatabase:
    return ProductDatabase(Product, Order, Wallet)


@alru_cache()
async def get_product_manager() -> ProductManager:
    product_db = await get_product_db()
    return ProductManager(product_db)
