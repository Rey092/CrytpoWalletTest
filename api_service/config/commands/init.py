# -*- coding: utf-8 -*-
import logging

from asgi_lifespan import LifespanManager

from api_service.apps.crypto.enums import AssetCode, AssetNetwork, AssetType
from api_service.apps.crypto.models import Asset
from api_service.config.db import SessionLocal

logger = logging.getLogger(__name__)


class ProjectInitialization:
    @classmethod
    async def start(cls, app):
        async with LifespanManager(app):
            await cls.create_assets()

    @classmethod
    async def create_assets(cls):
        db = SessionLocal()
        if not db.query(Asset).all():
            db_asset = Asset(
                code=AssetCode.ETH,
                network=AssetNetwork.ETHEREUM,
                type=AssetType.CURRENCY,
                decimals=10**18,
                is_currency=True,
            )
            db.add(db_asset)
            db.commit()
            db.refresh(db_asset)
            logger.info(f"Creating Asset {db_asset.code} in network {db_asset.network}")
        else:
            logger.info("Asset ETH in network ETHEREUM already exists")
