# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session

from apps.crypto.models import Asset


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
