# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from typing import Optional

import jwt

from config.settings import settings


class JWTBackend:
    """
    Set up the JWT Backend with the given cache backend and private key.
    """

    def __init__(self, access_expiration: int) -> None:
        self._access_expiration = access_expiration

    @staticmethod
    async def decode_token(token: str, leeway: int = 0) -> Optional[dict]:
        if token:
            try:
                payload = jwt.decode(
                    token,
                    settings.jwt_secret,
                    leeway=leeway,
                    algorithms=settings.jwt_algorithm,
                )
                return payload
            except Exception:
                return None
        return None

    @staticmethod
    def _create_token(
        payload: dict,
        expiration_delta: Optional[int],
    ) -> str:
        iat = datetime.utcnow()
        exp = datetime.utcnow() + timedelta(seconds=expiration_delta)
        payload.update({"iat": iat, "exp": exp})
        token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
        return token

    def create_access_token(self, payload: dict, access_expiration: bool) -> str:
        if access_expiration is True:
            return self._create_token(payload, settings.jwt_access_not_expiration)
        return self._create_token(payload, self._access_expiration)
