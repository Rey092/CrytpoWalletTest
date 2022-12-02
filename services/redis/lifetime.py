# -*- coding: utf-8 -*-


# from fastapi_limiter import FastAPILimiter


# async def init_redis(app: FastAPI) -> None:  # pragma: no cover
#     """
#     Creates connection pool for redis.
#
#     :param app: current fastapi application.
#
#     """
#     app.state.redis = await redis_from_url(
#         str(settings.redis_url),
#         max_connections=32,
#     )
#     # await FastAPILimiter.init(app.state.redis)
#
#
# async def shutdown_redis(app: FastAPI) -> None:  # pragma: no cover
#     """
#     Closes redis connection pool.
#
#     :param app: current FastAPI app.
#
#     """
#     await app.state.redis.connection_pool.disconnect()
