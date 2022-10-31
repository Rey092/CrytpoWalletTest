# -*- coding: utf-8 -*-
from uuid import UUID

from fastapi_helper.schemas.camel_schema import ApiSchema


# region Product
class ProductCreate(ApiSchema):
    wallet_id: UUID
    title: str
    image: str
    price: float


class ProductCreateResponse(ApiSchema):
    id: UUID
    image: str
    title: str
    address: str
    price: float


class ProductDetail(ApiSchema):
    id: UUID
    image: str
    title: str
    address: str
    price: float


# endregion Product


# region Order
class OrderCreate(ApiSchema):
    wallet_id: UUID


# endregion Order
