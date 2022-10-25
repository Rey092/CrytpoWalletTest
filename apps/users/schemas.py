# -*- coding: utf-8 -*-
from fastapi_helper.schemas.camel_schema import ApiSchema
from pydantic import EmailStr


class UserRegister(ApiSchema):
    email: EmailStr
    username: str
    password1: str
    password2: str


class UserLogin(ApiSchema):
    email: EmailStr
    password: str


class UserRegisterResponse(ApiSchema):
    detail: str = "Success! Welcome letter sent by email."
