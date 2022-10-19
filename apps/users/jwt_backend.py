# # -*- coding: utf-8 -*-
# from datetime import datetime, timedelta
# from typing import Optional
#
# import jwt
# from aioredis import Redis
# from async_lru import alru_cache
#
# from config.settings import settings
#
#
# class JWTBackend:
#     """
#     Set up the JWT Backend with the given cache backend and private key.
#     """
#
#     def __init__(
#         self,
#         cache_backend: Redis,
#         access_expiration: int,
#         refresh_expiration: int,
#     ) -> None:
#         self._cache = cache_backend
#         self._access_expiration = access_expiration
#         self._refresh_expiration = refresh_expiration
#
#     async def decode_token(self, token: str, leeway: int = 0) -> Optional[dict]:
#         if token:
#             try:
#                 payload = jwt.decode(
#                     token,
#                     settings.jwt_secret,
#                     leeway=leeway,
#                     algorithms=settings.jwt_algorithm,
#                 )
#                 return payload
#             except Exception:
#                 return None
#         return None
#
#     def _create_token(
#         self,
#         payload: dict,
#         token_type: str,
#         expiration_delta: Optional[int] = None,
#     ) -> str:
#         iat = datetime.utcnow()
#         if expiration_delta:
#             exp = datetime.utcnow() + timedelta(seconds=expiration_delta)
#         else:
#             exp = datetime.utcnow() + timedelta(seconds=60)
#
#         payload |= {"iat": iat, "exp": exp, "type": token_type}
#         token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
#         if isinstance(token, bytes):
#             # For PyJWT <= 1.7.1
#             return token.decode("utf-8")
#         # For PyJWT >= 2.0.0a1
#         return token
#
#     def create_access_token(self, payload: dict) -> str:
#         return self._create_token(payload, "access", self._access_expiration)
#
#     def create_refresh_token(self, payload: dict) -> str:
#         return self._create_token(payload, "refresh", self._refresh_expiration)
#
#     def create_tokens(self, payload: dict) -> dict:
#         access = self.create_access_token(payload)
#         refresh = self.create_refresh_token(payload)
#
#         return {"access": access, "refresh": refresh}
#
#
# @alru_cache()
# async def get_jwt_backend() -> JWTBackend:
#     """
#     Get the JWT Backend for the given request.
#     """
#     from config.app import app
#
#     return JWTBackend(
#         app.state.redis,
#         settings.jwt_access_expiration,
#         settings.jwt_refresh_expiration,
#     )
