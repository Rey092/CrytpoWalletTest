# -*- coding: utf-8 -*-
import inspect
from typing import Any, Type, Union
from uuid import UUID

from fastapi import File, Form, UploadFile
from fastapi_helper.schemas.camel_schema import ApiSchema
from pydantic import BaseModel, EmailStr
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


class UserRegister(ApiSchema):
    email: EmailStr
    username: str
    password1: str
    password2: str


class UserRegisterResponse(ApiSchema):
    id: UUID
    access_token: str


class UserLogin(ApiSchema):
    email: EmailStr
    password: str


class UserLoginResponse(ApiSchema):
    id: UUID
    access_token: str


class UserLogoutResponse(ApiSchema):
    message: str = "User logged out successfully"


class UserPayload(ApiSchema):
    id: UUID
    username: str
    avatar: Any


class UserGet(ApiSchema):
    id: UUID
    email: EmailStr
    username: str
    avatar: Any
    has_access_chat: bool
