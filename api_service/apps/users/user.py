# -*- coding: utf-8 -*-
from fastapi import Depends
from fastapi_helper.authorization.cookies_jwt_http_bearer import auth_bearer
from fastapi_helper.exceptions.auth_http_exceptions import InvalidCredentialsException
from sqlalchemy.orm import Session

from api_service.apps.users.dependencies import get_db, get_jwt_backend, get_user_manager
from api_service.apps.users.jwt_backend import JWTBackend
from api_service.apps.users.manager import UserManager
from api_service.apps.users.models import User
from api_service.apps.users.schemas import UserPayload


async def get_current_user_payload(
    token: str = Depends(auth_bearer),
    jwt_backend: JWTBackend = Depends(get_jwt_backend),
    manager: UserManager = Depends(get_user_manager),
    db: Session = Depends(get_db),
) -> UserPayload:
    try:
        payload = await jwt_backend.decode_token(token)
        if payload is None:
            raise InvalidCredentialsException()
        user = await manager.get_user(user_id=payload.get("id"), db=db)
        if not user:
            raise InvalidCredentialsException()
        return UserPayload(**payload, token=token)
    except Exception:
        raise InvalidCredentialsException()


async def get_current_user(
    payload: UserPayload = Depends(get_current_user_payload),
    manager: UserManager = Depends(get_user_manager),
    db: Session = Depends(get_db),
) -> User:
    user = await manager.get_user(user_id=payload.id, db=db)
    if not user:
        raise InvalidCredentialsException()
    return user
