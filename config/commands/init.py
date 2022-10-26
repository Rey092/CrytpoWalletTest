# -*- coding: utf-8 -*-
import logging

from sqlalchemy.orm import Session

from apps.crypto.crud import create_asset

# from asgi_lifespan import LifespanManager

# from apps.crypto.enums import AssetCode, AssetNetwork, AssetStandard, AssetType
# from apps.crypto.models import Asset
# from apps.users.models import Staff
# from config.settings import settings
# from config.utils.password_helper import password_helper

logger = logging.getLogger(__name__)


class ProjectInitialization:
    @classmethod
    async def start(cls, db: Session):
        await cls.create_assets(db)

    @staticmethod
    async def create_assets(db: Session):
        create_asset(db)


#
#     @classmethod
#     async def create_superuser(cls):
#         staff, created = await Staff.update_or_create(
#             is_superuser=True,
#             defaults={
#                 "email": settings.superuser_email,
#                 "password_hashed": password_helper.hash(settings.superuser_password),
#                 "full_name": settings.superuser_full_name,
#             },
#         )
#         logger.info(f"Superuser check. Created: {created}")
