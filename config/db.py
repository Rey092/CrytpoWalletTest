# -*- coding: utf-8 -*-
from typing import List

from config.settings import settings

MODELS_MODULES: List[str] = [
    "aerich.models",
    "apps.admin.models",
    "apps.users.models",
    "apps.crypto.models",
]
TORTOISE_CONFIG = {  # noqa: WPS407
    "connections": {
        "default": str(settings.db_url),
    },
    "apps": {
        "models": {
            "models": MODELS_MODULES,
            "default_connection": "default",
        },
    },
}
