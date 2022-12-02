# -*- coding: utf-8 -*-
import inspect
from enum import Enum
from typing import Type, Union
from uuid import UUID

from fastapi import File, Form, UploadFile
from fastapi_helper.schemas.camel_schema import ApiSchema
from pydantic import BaseModel
from pydantic.fields import ModelField


def as_form(cls: Type[BaseModel]):
    new_parameters = []

    for field_name, model_field in cls.__fields__.items():
        model_field: ModelField
        new_parameters.append(
            inspect.Parameter(
                model_field.alias,
                inspect.Parameter.POSITIONAL_ONLY,
                default=File(...) if model_field.required else File(model_field.default),
                annotation=model_field.outer_type_,
            )
            if model_field.type_ == UploadFile
            else inspect.Parameter(
                model_field.alias,
                inspect.Parameter.POSITIONAL_ONLY,
                default=Form(...) if model_field.required else Form(model_field.default),
                annotation=model_field.outer_type_,
            ),
        )

    async def as_form_func(**data):
        return cls(**data)

    sig = inspect.signature(as_form_func)
    sig = sig.replace(parameters=new_parameters)
    as_form_func.__signature__ = sig  # type: ignore
    setattr(cls, "as_form", as_form_func)
    return cls


@as_form
class UserUpdate(BaseModel):
    username: str
    profile_image: Union[UploadFile, None]
    password: Union[str, None]
    repeat_password: Union[str, None]
    delete: Union[bool, None]


# region Product
class WalletDetail(ApiSchema):
    id: UUID
    address: str
    balance: str


@as_form
class ProductCreate(ApiSchema):
    wallet_id: UUID
    title: str
    image: UploadFile
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
