# -*- coding: utf-8 -*-
from async_lru import alru_cache
from fastapi_helper.schemas.examples_generate import ExamplesGenerate

from apps.crypto.models import Wallet
from apps.product.database import ProductDatabase
from apps.product.manager import ProductManager
from apps.product.models import Order, Product
from apps.users.models import User
from config.db import SessionLocal
from config.web3_clients import EthereumProviderClient

examples_generate = ExamplesGenerate()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@alru_cache()
async def get_product_db() -> ProductDatabase:
    return ProductDatabase(Product, Order, Wallet, User)


@alru_cache()
async def get_ethereum_provider_client() -> EthereumProviderClient:
    return EthereumProviderClient()


@alru_cache()
async def get_product_manager() -> ProductManager:
    product_db = await get_product_db()
    ethereum_provider = await get_ethereum_provider_client()
    return ProductManager(product_db, ethereum_provider)
