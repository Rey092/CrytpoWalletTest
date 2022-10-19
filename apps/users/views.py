# -*- coding: utf-8 -*-
from fastapi import APIRouter
from pydantic import BaseModel

auth_router = APIRouter()


class User(BaseModel):
    email: str
    password: str


@auth_router.post("/login")
async def login(user: User):

    return user
