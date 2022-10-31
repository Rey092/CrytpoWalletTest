# -*- coding: utf-8 -*-
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from apps.crypto.dependencies import examples_generate, get_db, get_ethereum_manager
from apps.crypto.exceptions import (
    InvalidPrivateKeyException,
    InvalidRecipientException,
    InvalidSenderException,
    InvalidValueException,
    SendTransactionException,
    WalletAlreadyExistException,
)
from apps.crypto.manager import EthereumManager
from apps.crypto.schemas import (
    TransactionCreate,
    TransactionCreateResponse,
    TransactionDetail,
    WalletCreate,
    WalletCreateResponse,
    WalletDetail,
    WalletImport,
    WalletImportResponse,
)
from apps.users.models import User
from apps.users.user import get_current_user_payload

ethereum_router = APIRouter()


@ethereum_router.post(
    "/wallets/create",
    status_code=status.HTTP_201_CREATED,
    responses=examples_generate.get_error_responses(auth=True),
    response_model=WalletCreateResponse,
)
async def create_wallet(
    user: User = Depends(get_current_user_payload),
    db: Session = Depends(get_db),
    ethereum_manager: EthereumManager = Depends(get_ethereum_manager),
):
    """
    Create new wallet for user\n
    Permission: Is authenticated.
    """
    wallet = WalletCreate(user_id=str(user.id))
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
    user: User = Depends(get_current_user_payload),
    db: Session = Depends(get_db),
    ethereum_manager: EthereumManager = Depends(get_ethereum_manager),
):
    """
    Import existing wallet for user by private key\n
    Permission: Is authenticated.
    """
    wallet = WalletCreate(
        user_id=str(user.id),
        private_key=wallet_import.private_key,
    )
    return await ethereum_manager.import_existing_wallet(db=db, wallet=wallet)


@ethereum_router.get(
    "/wallets",
    responses=examples_generate.get_error_responses(auth=True),
    response_model=List[WalletDetail],
)
async def get_wallets(
    user: User = Depends(get_current_user_payload),
    db: Session = Depends(get_db),
    ethereum_manager: EthereumManager = Depends(get_ethereum_manager),
):
    """
    Get all user's wallets\n
    Permission: Is authenticated.
    """
    return await ethereum_manager.get_all_users_wallets(db=db, user_id=str(user.id))


@ethereum_router.get(
    "/transactions/{wallet_address}",
    responses=examples_generate.get_error_responses(auth=True),
    response_model=List[TransactionDetail],
)
async def get_transactions(
    wallet_address: str,
    user: User = Depends(get_current_user_payload),  # noqa
    db: Session = Depends(get_db),
    ethereum_manager: EthereumManager = Depends(get_ethereum_manager),
):
    """
    Get all transactions by wallet address\n
    Permission: Is authenticated.
    """
    return await ethereum_manager.get_transactions_by_wallet_address(db, wallet_address)


@ethereum_router.post(
    "/transactions/send",
    responses=examples_generate.get_error_responses(
        InvalidSenderException,
        InvalidRecipientException,
        SendTransactionException,
        InvalidValueException,
        auth=True,
    ),
    response_model=TransactionCreateResponse,
)
async def send_transaction(
    transaction: TransactionCreate,
    user: User = Depends(get_current_user_payload),  # noqa
    db: Session = Depends(get_db),
    ethereum_manager: EthereumManager = Depends(get_ethereum_manager),
):
    """
    Send ETH from your wallet to another wallet address\n
    Permission: Is authenticated.
    """
    return await ethereum_manager.send_transaction(db, transaction)
