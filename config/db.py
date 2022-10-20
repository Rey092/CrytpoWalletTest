# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.settings import settings

SQLALCHEMY_DATABASE_URL = str(settings.db_url)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# MODELS_MODULES: List[str] = [
#     "aerich.models",
#     "apps.admin.models",
#     "apps.users.models",
#     "apps.crypto.models",
# ]
# TORTOISE_CONFIG = {  # noqa: WPS407
#     "connections": {
#         "default": str(settings.db_url),
#     },
#     "apps": {
#         "models": {
#             "models": MODELS_MODULES,
#             "default_connection": "default",
#         },
#     },
# }
