# -*- coding: utf-8 -*-
from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from fastapi_helper.exceptions.auth_http_exceptions import InvalidCredentialsException, UnauthorizedException
from sqlalchemy.orm import Session
from starlette.requests import Request

from apps.users.dependencies import get_db, get_jwt_backend, get_user_manager
from apps.users.jwt_backend import JWTBackend
from apps.users.manager import UserManager
from apps.users.models import User
from apps.users.schemas import UserPayload


class OAuth2PasswordBearerCookie(OAuth2):
    async def __call__(self, request: Request) -> Optional[str]:
        cookie_authorization: str = request.cookies.get("Authorization")
        cookie_scheme, cookie_param = get_authorization_scheme_param(
            cookie_authorization,
        )
        if not cookie_authorization or cookie_scheme.lower() != "bearer":
            if self.auto_error:
                raise UnauthorizedException()
            else:
                return None
        return cookie_param


auth_bearer = OAuth2PasswordBearerCookie()


async def get_current_user_payload(
    token: str = Depends(auth_bearer),
    jwt_backend: JWTBackend = Depends(get_jwt_backend),
) -> UserPayload:
    try:
        payload = await jwt_backend.decode_token(token)
        if payload is None:
            raise InvalidCredentialsException()
        return UserPayload(**payload)
    except Exception:
        raise InvalidCredentialsException()


async def get_current_user(
    payload: UserPayload = Depends(get_current_user_payload),
    manager: UserManager = Depends(get_user_manager),
    db: Session = Depends(get_db),
) -> User:
    return await manager.get_user(user_id=payload.id, db=db)
