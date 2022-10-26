# -*- coding: utf-8 -*-
from fastapi.routing import APIRouter

from apps.crypto.views import ethereum_router
from apps.users.profile_views import profile_router
from apps.users.views import auth_router

api_router = APIRouter(prefix="/api")


# Users
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])


# Profile
api_router.include_router(profile_router, prefix="/profile", tags=["Profile"])


# Crypto
api_router.include_router(ethereum_router, prefix="/ethereum", tags=["Ethereum"])
