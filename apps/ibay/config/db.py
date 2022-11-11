# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.settings import settings

SQLALCHEMY_DATABASE_URL = str(settings.product_db_url)

engine_ibay = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=10, max_overflow=20)
SessionLocalIBay = sessionmaker(autocommit=False, autoflush=False, bind=engine_ibay)

BaseIBay = declarative_base()
