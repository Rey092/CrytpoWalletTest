# -*- coding: utf-8 -*-
from uuid import UUID

from fastapi_helper.schemas.camel_schema import ApiSchema


class UserRegister(ApiSchema):
    email: str
    username: str
    password1: str
    password2: str


class UserResponse(ApiSchema):
    id: UUID
    email: str
    username: str
