# -*- coding: utf-8 -*-
from typing import Any
from uuid import UUID

from fastapi_helper.schemas.camel_schema import ApiSchema
from pydantic import UUID4, EmailStr


class UserRegister(ApiSchema):
    email: EmailStr
    username: str
    password1: str
    password2: str


class UserRegisterResponse(ApiSchema):
    id: UUID
    access_token: str
    message: str = "Success! Welcome letter sent by email."


class UserLogin(ApiSchema):
    email: EmailStr
    password: str


class UserUpdate(ApiSchema):
    username: str


class UserLoginResponse(ApiSchema):
    id: UUID
    access_token: str


class UserLogoutResponse(ApiSchema):
    message: str = "Success!"


class UserPayload(ApiSchema):
    id: UUID4
    username: str
    avatar: Any


class UserGet(ApiSchema):
    id: UUID4
    email: EmailStr
    username: str
    avatar: Any
    has_access_chat: bool
