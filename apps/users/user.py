# -*- coding: utf-8 -*-
from fastapi import Depends
from fastapi_helper.authorization.cookies_jwt_http_bearer import auth_bearer
from fastapi_helper.exceptions.auth_http_exceptions import InvalidCredentialsException
from sqlalchemy.orm import Session

from apps.users.dependencies import get_db, get_jwt_backend, get_user_manager
from apps.users.jwt_backend import JWTBackend
from apps.users.manager import UserManager
from apps.users.models import User
from apps.users.schemas import UserPayload


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
