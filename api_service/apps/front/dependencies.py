# -*- coding: utf-8 -*-
from typing import Optional, Union

from fastapi import Depends
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request
from starlette.responses import RedirectResponse

from api_service.apps.users.dependencies import get_jwt_backend
from api_service.apps.users.jwt_backend import JWTBackend
from api_service.apps.users.schemas import UserPayload


class FrontEndBearerCookie(OAuth2):
    async def __call__(self, request: Request) -> Union[RedirectResponse, Optional[str]]:
        cookie_authorization: str = request.cookies.get("Authorization")
        cookie_scheme, cookie_param = get_authorization_scheme_param(
            cookie_authorization,
        )
        if not cookie_authorization or cookie_scheme.lower() != "bearer":
            if self.auto_error:
                return RedirectResponse("/auth/login")
            else:
                return None
        return cookie_param


auth_front_bearer = FrontEndBearerCookie()


async def check_user_token(
    token: str = Depends(auth_front_bearer),
    jwt_backend: JWTBackend = Depends(get_jwt_backend),
):
    try:
        payload = await jwt_backend.decode_token(token)
        if payload is None:
            return None
        return UserPayload(**payload)
    except Exception:
        return None
