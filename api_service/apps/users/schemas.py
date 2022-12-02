# -*- coding: utf-8 -*-
from typing import Any, List, Union
from uuid import UUID

from fastapi import UploadFile
from fastapi_helper.schemas.camel_schema import ApiSchema, as_form
from pydantic import BaseModel, EmailStr

from api_service.apps.product.schemas import WalletDetail


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
    remember_me: bool


class UserLoginResponse(ApiSchema):
    id: UUID
    access_token: str


class UserLogoutResponse(ApiSchema):
    message: str = "User logged out successfully"


class UserPayload(ApiSchema):
    id: UUID
    username: str
    avatar: Any
    token: Union[str, None]


class UserPermission(ApiSchema):
    has_access_chat: bool


class UserProfile(ApiSchema):
    id: UUID
    email: EmailStr
    username: str
    avatar: Union[str, None]
    permission: UserPermission
    count_messages: int
    wallets: List[WalletDetail]
