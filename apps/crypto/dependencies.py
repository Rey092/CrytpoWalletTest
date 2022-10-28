# -*- coding: utf-8 -*-
from async_lru import alru_cache
from fastapi_helper.schemas.examples_generate import ExamplesGenerate

from apps.crypto.database import EthereumDatabase
from apps.crypto.manager import EthereumManager
from apps.crypto.models import Asset, Transaction, Wallet
from apps.crypto.web3_client import EtherscanClient, InfuraClient
from apps.users.dependencies import get_jwt_backend
from config.db import SessionLocal


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
async def get_infura_client() -> InfuraClient:
    return InfuraClient()


@alru_cache()
async def get_ethereum_manager() -> EthereumManager:
    jwt_backend = await get_jwt_backend()
    ethereum_db = await get_ethereum_db()
    etherscan_client = await get_etherscan_client()
    infura_client = await get_infura_client()
    return EthereumManager(ethereum_db, jwt_backend, etherscan_client, infura_client)
