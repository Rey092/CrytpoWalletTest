# -*- coding: utf-8 -*-
from fastapi.routing import APIRouter

api_router = APIRouter(prefix="/api")

# Crypto
# api_router.include_router(crypto_router, prefix="/crypto", tags=["Crypto"])
# api_router.include_router(eth_router, prefix="/ethereum", tags=["Ethereum"])
# api_router.include_router(tron_router, prefix="/tron", tags=["Tron"])
# api_router.include_router(bitcoin_router, prefix="/btc", tags=["Bitcoin"])
# api_router.include_router(bnb_router, prefix="/bnb", tags=["Binance Smart Chain"])
# api_router.include_router(litecoin_router, prefix="/ltc", tags=["Litecoin"])

# Users
# api_router.include_router(crm_auth_router, prefix="/auth", tags=["Auth"])
# api_router.include_router(mobile_auth_router, prefix="/auth-mobile", tags=["MobileAuth"])
# api_router.include_router(superuser_router, prefix="/superuser", tags=["CRM Superuser"])
# api_router.include_router(staff_router, prefix="/staff", tags=["CRM Staff Profile"])
# api_router.include_router(users_router, prefix="/users", tags=["CRM Users"])
