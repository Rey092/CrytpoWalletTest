# -*- coding: utf-8 -*-
from fastapi_helper.schemas.camel_schema import ApiSchema


class WalletCreate(ApiSchema):
    wallet_number: str
    user_id: str
    private_key: str
    address: str
    balance: float
    asset: str
    network: str
