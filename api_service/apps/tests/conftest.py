# -*- coding: utf-8 -*-
from typing import AsyncGenerator

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from api_service.apps.tests.factories import create_user
from api_service.apps.users.dependencies import get_db
from api_service.apps.users.schemas import UserLogin, UserLoginResponse
from api_service.config.app import app
from api_service.config.db import Base, SessionLocal
from api_service.config.settings import settings


@pytest.fixture(scope="session")
def db_engine():
    """
    Creates engine SQLAlchemy and creates all tables in metadata
    :return: engine
    """
    engine = create_engine(str(settings.test_db_url))
    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="session")
def db(db_engine):
    """
    The fixture rolls back the session after each test.

    :param db_engine:
    :return: db

    """
    connection = db_engine.connect()

    # begin a non-ORM transaction
    connection.begin()

    # bind an individual Session to the connection
    db = Session(bind=connection)
    create_user(db)
    yield db
    db.rollback()
    connection.close()


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: backend name.

    """
    return "asyncio"


@pytest.fixture(scope="session")
async def fastapi_app() -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.

    """

    return app


@pytest.fixture(scope="session")
async def client(db: SessionLocal, fastapi_app: FastAPI) -> AsyncClient:
    """
    Fixture for creating HTTP client.

    :param db: Session of DB
    :param fastapi_app: FastAPI app.
    :return: HTTPX async client.

    """
    app.dependency_overrides[get_db] = lambda: db

    async with LifespanManager(fastapi_app):
        async with AsyncClient(app=fastapi_app, base_url=settings.backend_url) as client:
            yield client


@pytest.fixture(scope="session")
async def user_token(
    fastapi_app: FastAPI,
    client: AsyncClient,
) -> AsyncGenerator:
    """
    Fixture for user login and get token.
    """
    data = UserLogin(
        email=settings.user_email,
        password=settings.user_password,
        remember_me=True,
    )

    url = fastapi_app.url_path_for("login")
    response = await client.post(url, json=data.dict())
    assert response.status_code == 200
    yield UserLoginResponse(**response.json())
