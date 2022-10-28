# -*- coding: utf-8 -*-
from typing import Any
from uuid import UUID

from fastapi_helper.schemas.camel_schema import ApiSchema
from pydantic import EmailStr


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


class UserLoginResponse(ApiSchema):
    id: UUID
    access_token: str


class UserLogoutResponse(ApiSchema):
    message: str = "Success!"


class UserDetail(ApiSchema):
    id: UUID
    email: EmailStr
    username: str
    avatar: Any
    count_messages: Any
