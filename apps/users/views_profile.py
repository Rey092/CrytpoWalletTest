# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from fastapi_helper.schemas.examples_generate import examples_generate
from sqlalchemy.orm import Session
from starlette import status

from apps.users.dependencies import get_db, get_user_manager
from apps.users.manager import UserManager
from apps.users.models import User
from apps.users.schemas import UserProfile, UserUpdate
from apps.users.user import get_current_user

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


@profile_router.put("/update", response_model=UserProfile)
async def update_profile(
    user_data: UserUpdate = Depends(UserUpdate.as_form),
    user: User = Depends(get_current_user),
    user_manager: UserManager = Depends(get_user_manager),
    db: Session = Depends(get_db),
):
    """
    Update user profile\n
    Permission: Is authenticated.
    """
    user = await user_manager.update(
        user.id,
        user_data,
        db,
    )
    print(user_data)

    return user
