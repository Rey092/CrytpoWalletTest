# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session

from apps.crypto.models import Asset, Wallet
from apps.crypto.schemas import WalletCreate


def create_wallet(db: Session, wallet: WalletCreate):
    db_wallet = Wallet(
        wallet_address=wallet.wallet_address,
        user_id=wallet.user_id,
        private_key=wallet.private_key,
        balance=wallet.balance,
        asset_id=wallet.asset,
    )
    db.add(db_wallet)
    db.commit()
    db.refresh(db_wallet)
    return db_wallet


def create_asset(db: Session):
    db_asset = Asset(
        code="ETH",
        network="ETHEREUM",
        type="CURRENCY",
        decimals=10**18,
        is_currency=True,
    )
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset
