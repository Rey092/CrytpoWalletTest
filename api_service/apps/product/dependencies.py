# -*- coding: utf-8 -*-
from async_lru import alru_cache
from fastapi_helper.schemas.examples_generate import ExamplesGenerate

from api_service.api_service_producer import ApiServiceProducer
from api_service.apps.crypto.models import Transaction, Wallet
from api_service.apps.crypto.web3_clients import EthereumProviderClient
from api_service.apps.product.database import ProductDatabase
from api_service.apps.product.manager import ProductManager
from api_service.apps.product.models import Order, Product
from api_service.apps.users.dependencies import get_storage
from api_service.apps.users.models import User
from api_service.config.db import SessionLocal

examples_generate = ExamplesGenerate()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@alru_cache()
async def get_product_db() -> ProductDatabase:
    return ProductDatabase(Product, Order, Wallet, User, Transaction)


@alru_cache()
async def get_ethereum_provider_client() -> EthereumProviderClient:
    return EthereumProviderClient()


@alru_cache()
async def get_api_service_producer() -> ApiServiceProducer:
    return ApiServiceProducer()


@alru_cache()
async def get_product_manager() -> ProductManager:
    product_db = await get_product_db()
    ethereum_provider = await get_ethereum_provider_client()
    storage = await get_storage()
    api_service_producer = await get_api_service_producer()
    return ProductManager(product_db, ethereum_provider, storage, api_service_producer)
