# -*- coding: utf-8 -*-
# import os
import pathlib
from typing import List

import toml
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette import status
from starlette.responses import Response

# from apps.admin.endpoints import health
# from config.celery_utils import create_celery
from config.costum_logging import CustomizeLogger

# from config.db import TORTOISE_CONFIG
# from config.lifetime import register_shutdown_event, register_startup_event
from config.openapi import metadata_tags
from config.router import api_router

# from config.settings import settings
from config.utils.formatters import camel_case_split

# from starlette.staticfiles import StaticFiles
# from tortoise.contrib.fastapi import register_tortoise


def init_routers(app_: FastAPI) -> None:
    # app_.include_router(health.router, prefix="/health", tags=["Health"])
    app_.include_router(api_router)


def init_validation_handler(app_: FastAPI) -> None:
    # TODO: FIX
    @app_.exception_handler(RequestValidationError)
    async def http_exception_accept_handler(request: Request, exc: RequestValidationError) -> Response:
        data = [
            {
                "code": "validation-error",
                "type": exception["type"],
                "message": f"{camel_case_split(exception['loc'][1])}: {exception['msg']}"
                if exception["type"] != "value_error.jsondecode"
                else exception["msg"],
                "location": exception["loc"][0],
                "field": exception["loc"][1],
            }
            for exception in exc.errors()
        ]
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": data},
        )


def init_database(app_: FastAPI) -> None:
    # TODO: implement
    pass
    # register_tortoise(
    #     app_,
    #     config=TORTOISE_CONFIG,
    #     add_exception_handlers=True,
    #     generate_schemas=False,
    # )


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
    config_path = pathlib.Path(__file__).parent.with_name("logging_config.json")
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
        docs_url="/",
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
    init_validation_handler(app_=app_)
    init_database(app_=app_)

    init_cache()
    init_logging()

    return app_


app = create_app()
