# -*- coding: utf-8 -*-
from enum import Enum
from uuid import UUID

from fastapi_helper.schemas.camel_schema import ApiSchema


# region Product
class WalletDetail(ApiSchema):
    id: UUID
    address: str


class ProductCreate(ApiSchema):
    wallet_id: UUID
    title: str
    image: str
    price: float


class BaseProduct(ApiSchema):
    id: UUID
    image: str
    title: str
    price: str


class ProductDetail(BaseProduct):
    wallet: WalletDetail


# endregion Product


# region Order
class OrderCreate(ApiSchema):
    wallet_id: UUID
    product_id: UUID


class OrderDetail(ApiSchema):
    id: UUID
    product: BaseProduct
    txn_hash: str
    date: str
    status: Enum
    txn_hash_return: str = None


# endregion Order
