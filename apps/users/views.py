# -*- coding: utf-8 -*-
from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi_helper.schemas.examples_generate import examples_generate
from sqlalchemy.orm import Session
from starlette import status

from apps.users import schemas
from apps.users.dependencies import get_db, get_user_manager
from apps.users.exceptions import (
    EmailAlreadyExistException,
    EmailInvalidException,
    PasswordInvalidException,
    PasswordMismatchException,
    UsernameInvalidException,
)
from apps.users.manager import UserManager
from apps.users.schemas import UserLoginResponse, UserRegisterResponse
from apps.users.tasks import update_permission

auth_router = APIRouter()


@auth_router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserRegisterResponse,
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
    db: Session = Depends(get_db),
):
    result = await user_manager.create(user, db, background_tasks)
    result[0]["access_token"] = result[-1]
    background_tasks.add_task(update_permission, result[0]["id"], db, user_manager)
    return result[0]


@auth_router.post(
    "/login",
    response_model=UserLoginResponse,
    responses=examples_generate.get_error_responses(auth=True),
)
async def login(
    user: schemas.UserLogin,
    user_manager: UserManager = Depends(get_user_manager),
    db: Session = Depends(get_db),
):
    result = await user_manager.login(user, db)
    result[0]["access_token"] = result[-1]
    return result[0]
