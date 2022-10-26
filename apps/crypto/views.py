# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from apps.crypto.dependencies import examples_generate, get_db, get_ethereum_manager
from apps.crypto.exceptions import WalletAlreadyExistException
from apps.crypto.manager import EthereumManager
from apps.crypto.schemas import WalletCreate, WalletCreateResponse, WalletImport, WalletImportResponse

ethereum_router = APIRouter()


@ethereum_router.post(
    "/wallet/create",
    status_code=status.HTTP_201_CREATED,
    responses=examples_generate.get_error_responses(auth=True),
    response_model=WalletCreateResponse,
)
async def create_wallet(
    db: Session = Depends(get_db),
    ethereum_manager: EthereumManager = Depends(get_ethereum_manager),
):
    wallet = WalletCreate(user_id="a8b97433-da9e-4664-bf31-66cca01f5fb7")
    return await ethereum_manager.create_new_wallet(db=db, wallet=wallet)


@ethereum_router.post(
    "/wallet/import",
    status_code=status.HTTP_201_CREATED,
    responses=examples_generate.get_error_responses(
        WalletAlreadyExistException,
        auth=True,
    ),
    response_model=WalletImportResponse,
)
async def import_wallet(
    wallet_import: WalletImport,
    db: Session = Depends(get_db),
    ethereum_manager: EthereumManager = Depends(get_ethereum_manager),
):
    wallet = WalletCreate(
        user_id="a8b97433-da9e-4664-bf31-66cca01f5fb7",
        private_key=wallet_import.private_key,
    )
    return await ethereum_manager.import_existing_wallet(db=db, wallet=wallet)
