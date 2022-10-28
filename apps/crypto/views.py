# -*- coding: utf-8 -*-
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from apps.crypto.dependencies import examples_generate, get_db, get_ethereum_manager
from apps.crypto.exceptions import InvalidPrivateKeyException, WalletAlreadyExistException
from apps.crypto.manager import EthereumManager
from apps.crypto.schemas import (
    Transaction,
    Wallet,
    WalletCreate,
    WalletCreateResponse,
    WalletImport,
    WalletImportResponse,
)

ethereum_router = APIRouter()


@ethereum_router.post(
    "/wallets/create",
    status_code=status.HTTP_201_CREATED,
    responses=examples_generate.get_error_responses(auth=True),
    response_model=WalletCreateResponse,
)
async def create_wallet(
    db: Session = Depends(get_db),
    ethereum_manager: EthereumManager = Depends(get_ethereum_manager),
):
    """
    Create new wallet for user\n
    Permission: Is authenticated.
    """
    wallet = WalletCreate(user_id="a8b97433-da9e-4664-bf31-66cca01f5fb7")
    return await ethereum_manager.create_new_wallet(db=db, wallet=wallet)


@ethereum_router.post(
    "/wallets/import",
    status_code=status.HTTP_201_CREATED,
    responses=examples_generate.get_error_responses(
        WalletAlreadyExistException,
        InvalidPrivateKeyException,
        auth=True,
    ),
    response_model=WalletImportResponse,
)
async def import_wallet(
    wallet_import: WalletImport,
    db: Session = Depends(get_db),
    ethereum_manager: EthereumManager = Depends(get_ethereum_manager),
):
    """
    Import existing wallet for user by private key\n
    Permission: Is authenticated.
    """
    wallet = WalletCreate(
        user_id="a8b97433-da9e-4664-bf31-66cca01f5fb7",
        private_key=wallet_import.private_key,
    )
    return await ethereum_manager.import_existing_wallet(db=db, wallet=wallet)


@ethereum_router.get(
    "/wallets",
    responses=examples_generate.get_error_responses(auth=True),
    response_model=List[Wallet],
)
async def get_wallets(
    db: Session = Depends(get_db),
    ethereum_manager: EthereumManager = Depends(get_ethereum_manager),
):
    """
    Get all user's wallets\n
    Permission: Is authenticated.
    """
    return await ethereum_manager.get_all_users_wallets(db=db, user_id="a8b97433-da9e-4664-bf31-66cca01f5fb7")


@ethereum_router.get(
    "/transactions/{wallet_address}",
    responses=examples_generate.get_error_responses(auth=True),
    response_model=List[Transaction],
)
async def get_transactions(
    wallet_address: str,
    db: Session = Depends(get_db),
    ethereum_manager: EthereumManager = Depends(get_ethereum_manager),
):
    """
    Get all transactions by wallet address\n
    Permission: Is authenticated.
    """
    return await ethereum_manager.get_transactions_by_wallet_address(db, wallet_address)
