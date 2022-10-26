# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from apps.crypto import crud
from apps.crypto.schemas import WalletCreate
from apps.users.dependencies import get_db

ethereum_router = APIRouter()


@ethereum_router.post("/")
async def create_wallet(
    wallet: WalletCreate,
    db: Session = Depends(get_db),
):
    crud.create_wallet(db=db, wallet=wallet)
    return wallet
