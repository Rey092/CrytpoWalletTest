# -*- coding: utf-8 -*-
from fastapi import APIRouter
from pydantic import BaseModel

from fastapi_helper.schemas.examples import examples_generate
from sqlalchemy.orm import Session
from starlette import status

from apps.users import schemas
from apps.users.exceptions import (
    EmailAlreadyExistException,
    EmailInvalidException,
    PasswordInvalidException,
    PasswordMismatchException,
    UsernameInvalidException,
)
from apps.users.manager import get_user_manager
from config.db import SessionLocal

auth_router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class User(BaseModel):
    email: str
    password: str


@auth_router.post("/login")
async def login(user: schemas.UserLogin):
    manager = await get_user_manager()
    return await manager.login(user)


@auth_router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserRegisterResponse,
    responses=examples_generate.get_error_responses(
        EmailInvalidException,
        EmailAlreadyExistException,
        PasswordMismatchException,
        PasswordInvalidException,
        UsernameInvalidException,
    ),
)
async def register(user: schemas.UserRegister):
    manager = await get_user_manager()
    return await manager.create(user)
