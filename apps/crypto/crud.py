# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session

from apps.crypto.models import Wallet
from apps.crypto.schemas import WalletCreate


def create_wallet(db: Session, wallet: WalletCreate):
    db_wallet = Wallet(
        wallet_number=wallet.wallet_number,
        user_id=wallet.user_id,
        private_key=wallet.private_key,
        address=wallet.address,
        balance=wallet.balance,
        asset_id=wallet.asset,
        network=wallet.network,
    )
    db.add(db_wallet)
    db.commit()
    db.refresh(db_wallet)
    return db_wallet
