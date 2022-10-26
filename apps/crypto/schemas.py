# -*- coding: utf-8 -*-
from uuid import UUID

from fastapi_helper.schemas.camel_schema import ApiSchema


class AssetCreate(ApiSchema):
    id: UUID
    code: str
    network: str
    type: str
    standard: str = None
    decimals: int
    is_currency: bool


class WalletCreate(ApiSchema):
    wallet_address: str = None
    private_key: str = None
    user_id: str


class WalletImport(ApiSchema):
    private_key: str


class WalletCreateResponse(ApiSchema):
    message: str = "The new wallet has been successfully created."


class WalletImportResponse(WalletCreateResponse):
    message: str = "The wallet has been successfully imported."
