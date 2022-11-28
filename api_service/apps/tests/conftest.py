# -*- coding: utf-8 -*-
from typing import AsyncGenerator

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from api_service.apps.tests.test_database import SQLALCHEMY_DATABASE_URL
from api_service.apps.users.dependencies import get_db
from api_service.apps.users.schemas import UserLogin, UserLoginResponse
from api_service.config.app import app
from api_service.config.commands.init import ProjectInitialization
from api_service.config.db import Base
from api_service.config.settings import settings


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()

    # begin a non-ORM transaction
    # transaction = connection.begin()

    # bind an individual Session to the connection
    db = Session(bind=connection)
    # db = Session(db_engine)

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


@pytest.fixture
async def fastapi_app() -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.

    """

    await ProjectInitialization().start(app=app)

    return app


@pytest.fixture
async def client(db, fastapi_app: FastAPI) -> AsyncClient:
    """
    Fixture for creating HTTP client.

    :param fastapi_app: FastAPI app.
    :return: HTTPX async client.

    """
    app.dependency_overrides[get_db] = lambda: db

    async with LifespanManager(fastapi_app):
        async with AsyncClient(app=fastapi_app, base_url=settings.backend_url) as client:
            yield client


@pytest.fixture
async def user_token(
    fastapi_app: FastAPI,
    client: AsyncClient,
) -> AsyncGenerator:
    """
    Fixture for login as superuser and get tokens.
    """
    # prepare data
    data = UserLogin(
        email=settings.user_email,
        password=settings.user_password,
        remember_me=True,
    )

    # post data
    # url = fastapi_app.url_path_for("crm_auth:login")
    response = await client.post("/api/auth/login", json=data.dict())
    assert response.status_code == 200
    yield UserLoginResponse(**response.json())


# @pytest.fixture(autouse=True)
# async def initialize_db() -> AsyncGenerator[None, None]:
#     """
#     Initialize models and database.
#
#     :yields: Nothing.
#
#     """
#     initializer(
#         MODELS_MODULES,
#         db_url=str("sqlite://:memory"),
#         app_label="models",
#     )
#     register_tortoise(
#         app,
#         db_url=str("sqlite://:memory"),
#         modules={"models": MODELS_MODULES},
#     )
#
#     yield
#
#     await Tortoise.close_connections()
#     finalizer()
#
#
# # @pytest.fixture
# # async def test_rmq_pool() -> AsyncGenerator[Channel, None]:
# #     """
# #     Create rabbitMQ pool.
# #
# #     :yield: channel pool.
# #     """
# #     app_mock = Mock()
# #     init_rabbit(app_mock)
# #     yield app_mock.state.rmq_channel_pool
# #     await shutdown_rabbit(app_mock)
# #
# #
# # @pytest.fixture
# # async def test_exchange_name() -> str:
# #     """
# #     Name of an exchange to use in tests.
# #
# #     :return: name of an exchange.
# #     """
# #     return uuid.uuid4().hex
# #
# #
# # @pytest.fixture
# # async def test_routing_key() -> str:
# #     """
# #     Name of routing key to use whild binding test queue.
# #
# #     :return: key string.
# #     """
# #     return uuid.uuid4().hex
# #
# #
# # @pytest.fixture
# # async def test_exchange(
# #     test_exchange_name: str,
# #     test_rmq_pool: Pool[Channel],
# # ) -> AsyncGenerator[AbstractExchange, None]:
# #     """
# #     Creates test exchange.
# #
# #     :param test_exchange_name: name of an exchange to create.
# #     :param test_rmq_pool: channel pool for rabbitmq.
# #     :yield: created exchange.
# #     """
# #     async with test_rmq_pool.acquire() as conn:
# #         exchange = await conn.declare_exchange(
# #             name=test_exchange_name,
# #             auto_delete=True,
# #         )
# #         yield exchange
# #
# #         await exchange.delete(if_unused=False)
# #
# #
# # @pytest.fixture
# # async def test_queue(
# #     test_exchange: AbstractExchange,
# #     test_rmq_pool: Pool[Channel],
# #     test_routing_key: str,
# # ) -> AsyncGenerator[AbstractQueue, None]:
# #     """
# #     Creates queue connected to exchange.
# #
# #     :param test_exchange: exchange to bind queue to.
# #     :param test_rmq_pool: channel pool for rabbitmq.
# #     :param test_routing_key: routing key to use while binding.
# #     :yield: queue binded to test exchange.
# #     """
# #     async with test_rmq_pool.acquire() as conn:
# #         queue = await conn.declare_queue(name=uuid.uuid4().hex)
# #         await queue.bind(
# #             exchange=test_exchange,
# #             routing_key=test_routing_key,
# #         )
# #         yield queue
# #
# #         await queue.delete(if_unused=False, if_empty=False)
#
#
# @pytest.fixture
# async def fastapi_app() -> FastAPI:
#     """
#     Fixture for creating FastAPI app.
#
#     :return: fastapi app with mocked dependencies.
#
#     """
#     await ProjectInitialization().start(app=app)
#     return app
#
#
# @pytest.fixture
# async def client(fastapi_app: FastAPI) -> AsyncClient:
#     """
#     Fixture for creating HTTP client.
#
#     :param fastapi_app: FastAPI app.
#     :return: HTTPX async client.
#
#     """
#     async with LifespanManager(fastapi_app):
#         async with AsyncClient(app=fastapi_app, base_url=settings.backend_url) as client:
#             yield client
#
#
# @pytest.fixture
# async def superuser_tokens(
#     fastapi_app: FastAPI,
#     client: AsyncClient,
# ) -> AsyncGenerator[None, None]:
#     """
#     Fixture for login as superuser and get tokens.
#     """
#     # prepare data
#     data = StaffLoginSchema(
#         email=settings.superuser_email,
#         password=settings.superuser_password,
#     )
#
#     # post data in multipart/form-data
#     url = fastapi_app.url_path_for("crm_auth:login")
#     response = await client.post(url, json=data.dict())
#     assert response.status_code == 200
#
#     yield AccessRefreshTokensSchema(**response.json()["tokens"])
#
#
# @pytest.fixture
# async def new_staff(
#     fastapi_app: FastAPI,
#     client: AsyncClient,
#     superuser_tokens: AccessRefreshTokensSchema,
# ) -> AsyncGenerator[None, None]:
#     """
#     Fixture for creating new staff.
#     """
#     # prepare data
#     data = StaffCreateSchema(
#         email="test-example12345@gmail.com",
#         full_name="John Snow",
#         password="Password-0",
#     )
#
#     # post data in multipart/form-data
#     url = fastapi_app.url_path_for("superuser:staff_create")
#     response = await client.post(
#         url,
#         data=data.dict(by_alias=True),
#         headers={"Authorization": f"Bearer {superuser_tokens.access}"},
#     )
#     assert response.status_code == 201
#
#     # get user data
#     staff = await Staff.get(id=response.json()["id"])
#     assert staff.email == data.email
#     assert staff.full_name == data.full_name
#
#     yield staff
#
#
# @pytest.fixture
# async def new_staff_tokens(
#     fastapi_app: FastAPI,
#     client: AsyncClient,
#     new_staff: Staff,
# ) -> AsyncGenerator[None, None]:
#     """
#     Fixture for login (getting new staff access token).
#
#     :param new_staff: Staff object.
#     :param fastapi_app: FastAPI app.
#     :param client: HTTPX async client.
#
#     """
#     # prepare data
#     data = StaffLoginSchema(
#         email=new_staff.email,
#         password="Password-0",
#     )
#
#     # post data in multipart/form-data
#     url = fastapi_app.url_path_for("crm_auth:login")
#     response = await client.post(url, json=data.dict())
#     assert response.status_code == 200
#
#     yield AccessRefreshTokensSchema(**response.json()["tokens"])
