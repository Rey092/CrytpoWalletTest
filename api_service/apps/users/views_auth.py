# -*- coding: utf-8 -*-

from fastapi import APIRouter, BackgroundTasks, Depends, Response
from fastapi_helper.exceptions.auth_http_exceptions import UnauthorizedException
from fastapi_helper.schemas.examples_generate import examples_generate
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
from starlette import status

from api_service.apps.users import schemas
from api_service.apps.users.dependencies import get_db, get_user_manager
from api_service.apps.users.exceptions import (
    EmailAlreadyExistException,
    EmailInvalidException,
    PasswordInvalidException,
    PasswordMismatchException,
    UsernameInvalidException,
)
from api_service.apps.users.manager import UserManager
from api_service.apps.users.models import User
from api_service.apps.users.schemas import UserLogin, UserLoginResponse, UserLogoutResponse, UserRegisterResponse
from api_service.apps.users.tasks import update_permission
from api_service.apps.users.user import get_current_user
from api_service.config.settings import settings
from api_service.config.utils.rate_limiter import RateLimitException, rate_limit_callback

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
        RateLimitException,
    ),
    dependencies=[Depends(RateLimiter(times=4, seconds=60, callback=rate_limit_callback))],
)
async def register(
    user: schemas.UserRegister,
    response: Response,
    background_tasks: BackgroundTasks,
    user_manager: UserManager = Depends(get_user_manager),
    db: Session = Depends(get_db),
):
    result = await user_manager.create(user, db, background_tasks)
    result[0]["access_token"] = result[-1]
    user_id = result[0]["id"]
    response.set_cookie(
        key="Authorization",
        value=f'Bearer {result[0]["access_token"]}',
        expires=settings.jwt_access_not_expiration,
    )
    update_permission.apply_async(args=(user_id,), countdown=60)
    return result[0]


@auth_router.post(
    "/logout",
    response_model=UserLogoutResponse,
    responses=examples_generate.get_error_responses(
        UnauthorizedException,
        auth=False,
    ),
)
async def logout(response: Response, user: User = Depends(get_current_user)):
    response.delete_cookie("Authorization")
    return user


@auth_router.post(
    "/login",
    response_model=UserLoginResponse,
    responses=examples_generate.get_error_responses(
        RateLimitException,
        auth=True,
    ),
    dependencies=[Depends(RateLimiter(times=4, seconds=10, callback=rate_limit_callback))],
)
async def login(
    user: UserLogin,
    response: Response,
    user_manager: UserManager = Depends(get_user_manager),
    db: Session = Depends(get_db),
):
    """
    Login user in\n param rememberMe: if false access token expiration
    15 seconds.
    """
    result = await user_manager.login(user, db)
    result[0]["access_token"] = result[-1]
    response.set_cookie(
        key="Authorization",
        value=f'Bearer {result[0]["access_token"]}',
        expires=settings.jwt_access_not_expiration,
    )
    return result[0]
