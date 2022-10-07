# -*- coding: utf-8 -*-
import logging

from asgi_lifespan import LifespanManager

from apps.crypto.enums import AssetCode, AssetNetwork, AssetStandard, AssetType
from apps.crypto.models import Asset
from apps.users.models import Staff
from config.settings import settings
from config.utils.password_helper import password_helper

logger = logging.getLogger(__name__)


class ProjectInitialization:
    @classmethod
    async def start(cls, app):
        pass
        # async with LifespanManager(app):
        #     await cls.create_assets()
        #     await cls.create_superuser()

#     @classmethod
#     async def create_assets(cls):
#         cryptos = [
#             Asset(
#                 code=AssetCode.ETH,
#                 network=AssetNetwork.ETHEREUM,
#                 type=AssetType.CURRENCY,
#                 standard=None,
#                 decimals=10**18,
#                 is_currency=True,
#             ),
#             Asset(
#                 code=AssetCode.USDT,
#                 network=AssetNetwork.ETHEREUM,
#                 type=AssetType.TOKEN,
#                 standard=AssetStandard.ERC20,
#                 decimals=10**6,
#                 is_currency=False,
#             ),
#             Asset(
#                 code=AssetCode.USDC,
#                 network=AssetNetwork.ETHEREUM,
#                 type=AssetType.TOKEN,
#                 standard=AssetStandard.ERC20,
#                 decimals=10**6,
#                 is_currency=False,
#             ),
#             Asset(
#                 code=AssetCode.TRX,
#                 network=AssetNetwork.TRON,
#                 type=AssetType.CURRENCY,
#                 standard=None,
#                 decimals=10**6,
#                 is_currency=True,
#             ),
#             Asset(
#                 code=AssetCode.USDT,
#                 network=AssetNetwork.TRON,
#                 type=AssetType.TOKEN,
#                 standard=AssetStandard.TRC20,
#                 decimals=10**6,
#                 is_currency=False,
#             ),
#             Asset(
#                 code=AssetCode.USDC,
#                 network=AssetNetwork.TRON,
#                 type=AssetType.TOKEN,
#                 standard=AssetStandard.TRC20,
#                 decimals=10**6,
#                 is_currency=False,
#             ),
#             Asset(
#                 code=AssetCode.BTC,
#                 network=AssetNetwork.BITCOIN,
#                 type=AssetType.CURRENCY,
#                 standard=None,
#                 decimals=10**8,
#                 is_currency=True,
#             ),
#             Asset(
#                 code=AssetCode.LTC,
#                 network=AssetNetwork.LITECOIN,
#                 type=AssetType.CURRENCY,
#                 standard=None,
#                 decimals=10**8,
#                 is_currency=True,
#             ),
#             Asset(
#                 code=AssetCode.BNB,
#                 network=AssetNetwork.BINANCE,
#                 type=AssetType.CURRENCY,
#                 standard=None,
#                 decimals=10**18,
#                 is_currency=True,
#             ),
#         ]
#
#         for crypto in cryptos:
#             # if crypto with this code and network already exists, skip it
#             if await Asset.get_or_none(code=crypto.code.value, network=crypto.network.value):
#                 logger.info(f"Asset {crypto.code} in network {crypto.network} already exists")
#             else:
#                 logger.info(f"Creating Asset {crypto.code} in network {crypto.network}")
#                 await crypto.save()
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
