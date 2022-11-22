# -*- coding: utf-8 -*-
import aioredis
from aioredis import Redis

from api_service.config.settings import settings


async def get_redis() -> Redis:
    redis = aioredis.from_url(
        url=str(settings.redis_url),
        encoding="utf8",
        decode_responses=True,
    )
    return redis
