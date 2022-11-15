# -*- coding: utf-8 -*-
import logging

from asgi_lifespan import LifespanManager
from faker import Faker
from fastapi_helper.utilities.password_helper import PasswordHelper

from api_service.apps.crypto.enums import AssetCode, AssetNetwork, AssetType
from api_service.apps.crypto.models import Asset
from api_service.apps.users.models import Permission, User
from api_service.config.db import SessionLocal

logger = logging.getLogger(__name__)
pass_helper = PasswordHelper()
fake = Faker("ru_RU")


class ProjectInitialization:
    @classmethod
    async def start(cls, app):
        async with LifespanManager(app):
            await cls.create_assets()
            await cls.create_users()

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

    @classmethod
    async def create_users(cls):
        db = SessionLocal()
        if not db.query(User).all():
            for i in range(3):
                db_user = User(
                    email=fake.free_email(),
                    username=f"{fake.first_name_male()} {fake.last_name_male()}",
                    password=pass_helper.hash("Zaqwerty123@"),
                )
                db.add(db_user)
                db.commit()
                db.refresh(db_user)

                db_permission = Permission(has_access_chat=True, user_id=db_user.id)
                db.add(db_permission)
                db.commit()
                db.refresh(db_permission)
                logger.info(f"Created new user: {db_user.username}")
        else:
            logger.info("Users already exists")
