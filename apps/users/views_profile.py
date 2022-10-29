# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from apps.crypto.dependencies import get_ethereum_manager
from apps.crypto.manager import EthereumManager
from apps.users import schemas
from apps.users.dependencies import get_db, get_user_manager
from apps.users.manager import UserManager
from apps.users.models import User
from apps.users.user import get_current_user

profile_router = APIRouter()


@profile_router.get("/")
async def get_profile(
    user=Depends(get_current_user),
    user_manager: UserManager = Depends(get_user_manager),
    ethereum_manager: EthereumManager = Depends(get_ethereum_manager),
    db: Session = Depends(get_db),
):
    # wallet = await ethereum_manager.get_all_users_wallets(db, user.id)
    user = await user_manager.get_user(user.id, db)
    return user


@profile_router.put("/")
async def update_profile(
    user_data: schemas.UserUpdate,
    user: User = Depends(get_current_user),
    user_manager: UserManager = Depends(get_user_manager),
    db: Session = Depends(get_db),
):
    result = await user_manager.update(user.id, user_data, db)

    return result
