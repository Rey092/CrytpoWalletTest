# -*- coding: utf-8 -*-
from async_lru import alru_cache
from fastapi_helper.schemas.examples_generate import ExamplesGenerate

from api_service.apps.crypto.api_service_producer import ApiServiceProducer
from api_service.apps.crypto.database import EthereumDatabase
from api_service.apps.crypto.manager import EthereumManager
from api_service.apps.crypto.models import Asset, Transaction, Wallet
from api_service.apps.crypto.web3_clients import EthereumProviderClient, EtherscanClient
from api_service.config.db import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


examples_generate = ExamplesGenerate()


@alru_cache()
async def get_ethereum_db() -> EthereumDatabase:
    return EthereumDatabase(Wallet, Asset, Transaction)


@alru_cache()
async def get_etherscan_client() -> EtherscanClient:
    return EtherscanClient()


@alru_cache()
async def get_ethereum_provider_client() -> EthereumProviderClient:
    return EthereumProviderClient()


@alru_cache()
async def get_api_service_producer() -> ApiServiceProducer:
    return ApiServiceProducer()


@alru_cache()
async def get_ethereum_manager() -> EthereumManager:
    ethereum_db = await get_ethereum_db()
    etherscan_client = await get_etherscan_client()
    ethereum_provider = await get_ethereum_provider_client()
    api_service_producer = await get_api_service_producer()
    return EthereumManager(ethereum_db, etherscan_client, ethereum_provider, api_service_producer)
