# -*- coding: utf-8 -*-
from aioredis import Redis
from fastapi import APIRouter, Depends

from services.redis.dependency import get_redis
from services.redis.schemas import RedisValueDTO

router = APIRouter()


@router.get("/", tags=["Health"])
async def health_check() -> None:
    """
    Checks the health of a project.

    It returns 200 if the project is healthy.

    """


@router.get("/redis-get/", response_model=RedisValueDTO, tags=["Health"])
async def get_redis_value(
    key: str,
    redis: Redis = Depends(get_redis),
) -> RedisValueDTO:
    """
    Get value from redis.

    :param key: redis key, to get data from.
    :param redis: redis connection with pool.
    :returns: information from redis.

    """
    redis_value = await redis.get(key)
    return RedisValueDTO(
        key=key,
        value=redis_value,
    )


@router.put("/redis-set/", tags=["Health"])
async def set_redis_value(
    redis_value: RedisValueDTO,
    redis: Redis = Depends(get_redis),
) -> None:
    """
    Set value in redis.

    :param redis_value: new value data.
    :param redis: redis connection with pool.

    """
    if redis_value.value is not None:
        await redis.set(name=redis_value.key, value=redis_value.value)
