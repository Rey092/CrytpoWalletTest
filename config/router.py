# -*- coding: utf-8 -*-
from fastapi.routing import APIRouter

from apps.crypto.views import ethereum_router
from apps.product.views import product_router
from apps.users.views_auth import auth_router
from apps.users.views_profile import profile_router

api_router = APIRouter(prefix="/api")


# Users
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])


# Profile
api_router.include_router(profile_router, prefix="/profile", tags=["Profile"])


# Crypto
api_router.include_router(ethereum_router, prefix="/ethereum", tags=["Ethereum"])


# IBay
api_router.include_router(product_router, prefix="/ibay", tags=["IBay"])
