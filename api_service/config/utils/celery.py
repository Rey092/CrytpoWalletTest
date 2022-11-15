# -*- coding: utf-8 -*-
import asyncio
from typing import Callable

from tortoise import Tortoise

from api_service.config.db import TORTOISE_CONFIG


async def wrap_db_ctx(func: Callable, *args, **kwargs) -> None:
    try:
        await Tortoise.init(
            config=TORTOISE_CONFIG,
        )
        await func(*args, **kwargs)
    finally:
        await Tortoise.close_connections()


def async_to_sync(func: Callable, *args, **kwargs) -> None:
    asyncio.run(wrap_db_ctx(func, *args, **kwargs))
