# -*- coding: utf-8 -*-
from api_service.config.settings import settings

metadata_tags = [
    {
        "name": "Auth",
        "description": "Authentication and authorization for users.",
    },
    {
        "name": "Ethereum",
        "description": "Create and import wallets. Get all wallets. Get transactions by wallet. Send transaction",
    },
    {
        "name": "Profile",
        "description": "Get and update user profile.",
    },
    {
        "name": "IBay",
        "description": "Create product. Get All product. Create order on product. Get all user's orders.",
    },
    {
        "name": "Chat Service",
        "description": "Documents for chat.",
        "externalDocs": {
            "description": "Asyncapi Docs",
            "url": settings.backend_url + settings.asyncapi_docs_url,
        },
    },
]
