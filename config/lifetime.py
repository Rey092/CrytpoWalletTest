# -*- coding: utf-8 -*-
from typing import Awaitable, Callable

from fastapi import FastAPI

from services.admin.lifetime import init_admin

from services.rabbit.lifetime import init_rabbit, shutdown_rabbit
from services.redis.lifetime import init_redis, shutdown_redis


def register_startup_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application startup.

    This function uses fastAPI app to store data
    in the state, such as db_engine.

    :param app: the fastAPI application.
    :return: function that actually performs actions.

    """

    @app.on_event("startup")
    async def _startup() -> None:  # noqa: WPS430
        await init_redis(app)
        await init_rabbit(app)
        await init_admin(app)

    return _startup


def register_shutdown_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application's shutdown.

    :param app: fastAPI application.
    :return: function that actually performs actions.

    """

    @app.on_event("shutdown")
    async def _shutdown() -> None:  # noqa: WPS430
        await shutdown_redis(app)
        await shutdown_rabbit(app)

    return _shutdown
