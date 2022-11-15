# -*- coding: utf-8 -*-
from math import ceil

from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_429_TOO_MANY_REQUESTS

from api_service.config.openapi import ApiError

RATE_LIMIT_ERROR = ApiError(
    code="ratelimit-001",
    type="TOO_MANY_REQUESTS",
    message="Too Many Requests.",
    exception=Exception,
    status_code=HTTP_429_TOO_MANY_REQUESTS,
)


async def rate_limit_callback(request: Request, response: Response, pexpire: int):  # noqa
    """
    default callback when too many requests.

    :param request:
    :param pexpire: The remaining milliseconds
    :param response:
    :return:

    """
    expire = ceil(pexpire / 1000)
    raise RATE_LIMIT_ERROR.http_exception(headers={"Retry-After": str(expire)})
