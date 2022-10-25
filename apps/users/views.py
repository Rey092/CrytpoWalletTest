# -*- coding: utf-8 -*-
import time

from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi_helper.schemas.examples import examples_generate
from pydantic import BaseModel
from starlette import status

from apps.users import schemas
from apps.users.dependencies import get_user_manager
from apps.users.exceptions import (
    EmailAlreadyExistException,
    EmailInvalidException,
    PasswordInvalidException,
    PasswordMismatchException,
    UsernameInvalidException,
)
from apps.users.manager import UserManager
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


def write_notification():
    time.sleep(5)
    print("ok")


@auth_router.post("/login")
async def login(
    user: schemas.UserLogin,
    background_tasks: BackgroundTasks,
    user_manager: UserManager = Depends(get_user_manager),
):
    background_tasks.add_task(write_notification)

    return await user_manager.login(user)


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
async def register(
    user: schemas.UserRegister,
    background_tasks: BackgroundTasks,
    user_manager: UserManager = Depends(get_user_manager),
):
    return await user_manager.create(user, background_tasks)
