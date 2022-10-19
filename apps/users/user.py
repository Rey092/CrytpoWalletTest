# # -*- coding: utf-8 -*-
# from typing import Optional
#
# from fastapi import Depends
#
# from apps.users.api_errors import AuthApiErrors
# from apps.users.jwt_backend import get_jwt_backend
# from apps.users.models import User
# from apps.users.schemas import UserPayload
# from config.openapi import jwt_http_bearer, jwt_http_bearer_no_error
#
# # async def get_authenticated_user(
# #         request: Request,
# #         token: str = Depends(oauth2_scheme),
# #         jwt_backend=Depends(get_jwt_backend),
# # ) -> User:
# #     print(token)
# #     result = await jwt_backend.decode_token(token)
# #     if not result:
# #         raise AuthApiErrors.INVALID_CREDENTIALS.http_exception()
# #     user = await User.get(id=result["id"], email=result["email"])
# #     if not user:
# #         raise Exception("User not found")
# #
# #     return user
#
#
# async def get_user_payload(
#     jwt_backend=Depends(get_jwt_backend),
#     bearer: Optional[str] = Depends(jwt_http_bearer_no_error),
# ) -> Optional[UserPayload]:
#     if bearer:
#         if token := bearer.credentials:  # noqa
#             if data := await jwt_backend.decode_token(token):
#                 return UserPayload(**data)
#             raise AuthApiErrors.INVALID_CREDENTIALS.http_exception()
#
#     return None
#
#
# async def get_user(
#     user_payload: Optional[UserPayload] = Depends(get_user_payload),
# ) -> Optional[User]:
#     if user_payload:
#         return await user_payload.get_instance()
#
#     return None
#
#
# async def get_authenticated_user_payload(
#     jwt_backend=Depends(get_jwt_backend),
#     bearer: str = Depends(jwt_http_bearer),
# ) -> UserPayload:
#     if token := bearer.credentials:  # noqa
#         if data := await jwt_backend.decode_token(token):
#             return UserPayload(**data)
#         raise AuthApiErrors.INVALID_CREDENTIALS.http_exception()
#     raise AuthApiErrors.NOT_AUTHENTICATED.http_exception()
#
#
# async def get_authenticated_user(
#     user_payload: UserPayload = Depends(get_authenticated_user_payload),
# ) -> User:
#     user = await user_payload.get_instance()
#     return user
