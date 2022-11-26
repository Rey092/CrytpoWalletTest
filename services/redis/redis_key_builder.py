# -*- coding: utf-8 -*-
import hashlib
from typing import Callable, Optional

from fastapi_cache import FastAPICache
from starlette.requests import Request
from starlette.responses import Response


def my_key_builder(
    func: Callable,
    namespace: Optional[str] = "",
    request: Request = None,
    response: Response = None,
    *args,
    **kwargs,
):
    prefix = f"{FastAPICache.get_prefix()}:{namespace}:"
    cache_key = prefix + hashlib.md5(f"{func.__module__}:{func.__name__}:{args}:{kwargs}".encode()).hexdigest()
    return cache_key
