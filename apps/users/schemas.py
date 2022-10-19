# -*- coding: utf-8 -*-
# TODO: fastapi_helper base schema
from pydantic import BaseModel


class UserLogin(BaseModel):
    email: str
    password: str


class UserRegister(BaseModel):
    email: str
    password: str
