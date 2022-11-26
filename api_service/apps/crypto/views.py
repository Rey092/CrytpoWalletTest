# -*- coding: utf-8 -*-
import json
from typing import Any, List

from fastapi import APIRouter, Depends
from fastapi_cache import JsonCoder
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
from starlette import status

from api_service.apps.crypto.dependencies import (
    examples_generate,
    get_db,
    get_ethereum_manager,
    get_fastapi_cache_backend,
    get_fastapi_cache_coder,
)
from api_service.apps.crypto.exceptions import (
    InvalidPrivateKeyException,
    InvalidRecipientException,
    InvalidSenderException,
    InvalidValueException,
    SendTransactionException,
    WalletAlreadyExistException,
)
from api_service.apps.crypto.manager import EthereumManager
from api_service.apps.crypto.schemas import (
    TransactionCreate,
    TransactionCreateResponse,
    TransactionDetail,
    WalletCreate,
    WalletCreateResponse,
    WalletDetail,
    WalletImport,
    WalletImportResponse,
)
from api_service.apps.users.models import User
from api_service.apps.users.user import get_current_user_payload
from api_service.config.utils.rate_limiter import RateLimitException, rate_limit_callback
from services.redis.redis_key_builder import my_key_builder

ethereum_router = APIRouter()


@ethereum_router.post(
    "/wallets/create",
    dependencies=[Depends(RateLimiter(times=2, seconds=60, callback=rate_limit_callback))],
    status_code=status.HTTP_201_CREATED,
    responses=examples_generate.get_error_responses(
        RateLimitException,
        auth=True,
    ),
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
    dependencies=[Depends(RateLimiter(times=2, seconds=30, callback=rate_limit_callback))],
    status_code=status.HTTP_201_CREATED,
    responses=examples_generate.get_error_responses(
        WalletAlreadyExistException,
        InvalidPrivateKeyException,
        RateLimitException,
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
    cache_backend: Any = Depends(get_fastapi_cache_backend),
    cache_coder: JsonCoder = Depends(get_fastapi_cache_coder),
    user: User = Depends(get_current_user_payload),  # noqa
    db: Session = Depends(get_db),
    ethereum_manager: EthereumManager = Depends(get_ethereum_manager),
):
    """
    Get all transactions by wallet address\n
    Permission: Is authenticated.
    """
    cache_key = my_key_builder(get_transactions, f"wallet-history:{wallet_address}")
    cache = await cache_backend.get(cache_key)
    if cache:
        return json.loads(cache)
    transactions = await ethereum_manager.get_transactions_by_wallet_address(db, wallet_address)
    await cache_backend.set(cache_key, cache_coder.encode(transactions), expire=60 * 60 * 2)
    return transactions


@ethereum_router.post(
    "/transactions/send",
    dependencies=[Depends(RateLimiter(times=1, seconds=5, callback=rate_limit_callback))],
    responses=examples_generate.get_error_responses(
        InvalidSenderException,
        InvalidRecipientException,
        SendTransactionException,
        InvalidValueException,
        RateLimitException,
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
