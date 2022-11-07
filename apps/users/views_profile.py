# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Response
from fastapi_helper.schemas.examples_generate import examples_generate
from sqlalchemy.orm import Session
from starlette import status

from apps.users.dependencies import get_db, get_user_manager
from apps.users.exceptions import (
    DeleteImageInvalidException,
    PasswordInvalidException,
    PasswordMismatchException,
    UsernameInvalidException,
)
from apps.users.manager import UserManager
from apps.users.schemas import UserPayload, UserProfile, UserUpdate
from apps.users.user import get_current_user, get_current_user_payload
from config.settings import settings
from config.storage import StorageException, ValidateFormatException

profile_router = APIRouter()


@profile_router.get(
    "/get",
    status_code=status.HTTP_200_OK,
    responses=examples_generate.get_error_responses(auth=True),
    response_model=UserProfile,
)
async def get_profile(
    user=Depends(get_current_user),
):
    """
    Get user profile\n
    Permission: Is authenticated.
    """
    return user


@profile_router.put(
    "/update",
    status_code=status.HTTP_200_OK,
    responses=examples_generate.get_error_responses(
        UsernameInvalidException,
        PasswordMismatchException,
        StorageException,
        ValidateFormatException,
        DeleteImageInvalidException,
        PasswordInvalidException,
        auth=True,
    ),
    response_model=UserProfile,
)
async def update_profile(
    response: Response,
    user_data: UserUpdate = Depends(UserUpdate.as_form),
    user: UserPayload = Depends(get_current_user_payload),
    user_manager: UserManager = Depends(get_user_manager),
    db: Session = Depends(get_db),
):
    """
    Update user profile\n
    Permission: Is authenticated.
    """
    result = await user_manager.update(
        user.id,
        user.token,
        user_data,
        db,
    )
    response.set_cookie(
        key="Authorization",
        value=f"Bearer {result[-1]}",
        expires=settings.jwt_access_not_expiration,
    )
    return result[0]
