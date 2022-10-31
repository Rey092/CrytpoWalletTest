# -*- coding: utf-8 -*-
from fastapi.routing import APIRouter

from apps.front.auth_views import auth_front_router
from apps.front.profile_views import profile_front_router

front_router = APIRouter()


# Users
front_router.include_router(auth_front_router, prefix="/auth")

# Profile
front_router.include_router(profile_front_router, prefix="/profile")

#
# # Crypto
# front_router.include_router(ethereum_router, prefix="/ethereum", tags=["Ethereum"])