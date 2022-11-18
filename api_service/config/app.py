# -*- coding: utf-8 -*-
# import os
import pathlib
from typing import List

import toml
from fastapi import FastAPI, Request
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_helper import DefaultHTTPException
from fastapi_helper.exceptions.validation_exceptions import init_validation_handler
from starlette.staticfiles import StaticFiles

from api_service.api_service_consumer import api_consumer_thread
from api_service.apps.crypto.wallets_balance_parser import parsing_balances_thread
from api_service.apps.front.router import front_router
from api_service.apps.users import models
from api_service.config.costum_logging import CustomizeLogger
from api_service.config.db import engine
from api_service.config.openapi import metadata_tags
from api_service.config.router import api_router

# from config.settings import settings

# from starlette.staticfiles import StaticFiles
# from tortoise.contrib.fastapi import register_tortoise


def init_routers(app_: FastAPI) -> None:
    app_.include_router(api_router)
    app_.include_router(front_router)


def init_database() -> None:
    models.Base.metadata.create_all(bind=engine)


def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        # Middleware(SQLAlchemyMiddleware),
    ]
    return middleware


def init_cache() -> None:
    pass
    # Cache.init(backend=RedisBackend(), key_maker=CustomKeyMaker())


def init_logging() -> None:
    config_path = pathlib.Path(__file__).parent.parent.with_name("logging_config.json")
    CustomizeLogger.make_logger(config_path)


# extract title from pyproject.toml
def get_project_data() -> dict:
    pyproject_path = pathlib.Path("pyproject.toml")
    pyproject_data = toml.load(pyproject_path.open())
    poetry_data = pyproject_data["tool"]["poetry"]
    return poetry_data


def create_app() -> FastAPI:
    poetry_data = get_project_data()

    app_ = FastAPI(
        title=poetry_data["name"],
        description=poetry_data["description"],
        version=poetry_data["version"],
        docs_url="/docs",
        redoc_url="/redoc",
        middleware=make_middleware(),
        openapi_tags=metadata_tags,
    )

    # app_.celery_app = create_celery()

    # Adds startup and shutdown events.
    # register_startup_event(app_)
    # register_shutdown_event(app_)

    # Initialize other utils.
    init_routers(app_=app_)
    init_validation_handler(app=app_)
    init_database()

    init_cache()
    init_logging()

    # Start needed threads
    api_consumer_thread.start()
    parsing_balances_thread.start()

    app_.mount("/static", StaticFiles(directory="static"), name="static")

    return app_


app = create_app()


@app.exception_handler(DefaultHTTPException)
async def http_exception_accept_handler(request: Request, exc: DefaultHTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=[{"code": exc.code, "type": exc.type, "message": exc.message}],
    )