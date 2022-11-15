# -*- coding: utf-8 -*-
from fastapi.routing import APIRouter

from api_service.apps.front.auth_views import auth_front_router
from api_service.apps.front.chat_views import chat_front_router
from api_service.apps.front.ibay_views import ibay_front_router
from api_service.apps.front.profile_views import profile_front_router
from api_service.apps.front.wallet_views import wallets_front_router

front_router = APIRouter()


# Users
front_router.include_router(auth_front_router, prefix="/auth")

# Profile
front_router.include_router(profile_front_router, prefix="/profile")

# Crypto
front_router.include_router(wallets_front_router, prefix="/wallets")
front_router.include_router(ibay_front_router, prefix="/ibay")

# Chat
front_router.include_router(chat_front_router, prefix="/chat")
