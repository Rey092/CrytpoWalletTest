# -*- coding: utf-8 -*-
from fastapi.routing import APIRouter

from apps.users.profile_views import profile_router
from apps.users.views import auth_router

api_router = APIRouter(prefix="/api")

# Crypto
# api_router.include_router(eth_router, prefix="/ethereum", tags=["Ethereum"])


# Users
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])

# Profile
api_router.include_router(profile_router, prefix="/profile", tags=["Profile"])
