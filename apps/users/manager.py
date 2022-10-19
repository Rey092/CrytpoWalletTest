# # -*- coding: utf-8 -*-
# import hashlib
#
# from async_lru import alru_cache
# from email_validator import validate_email
# from fastapi.encoders import jsonable_encoder
# from passlib.pwd import genword
# from starlette.background import BackgroundTasks
#
# from config.settings import settings
# from config.utils import EmailSchema
# from config.utils.email_client import create_email_client
# from config.utils.password_helper import PasswordHelper, password_helper
#
# from .api_errors import AuthApiErrors
# from .database import TortoiseUserDatabase
# from .jwt_backend import JWTBackend, get_jwt_backend
# from .models import User
# from .schemas import UserCreateSchema, UserLoginSchema, UserPayload, user_db
#
#
# class UserManager:
#     reset_password_token_secret = settings.jwt_secret
#     verification_token_secret = settings.jwt_secret
#
#     def __init__(
#         self,
#         database: TortoiseUserDatabase,
#         jwt_backend: JWTBackend,
#         pass_helper: "PasswordHelper",
#     ):
#         self.user_db = database
#         self.jwt_backend = jwt_backend
#         self.password_helper = pass_helper
#
#     @staticmethod
#     async def on_after_register(user: User):
#         print(f"User {user.id} has registered.")
#
#     @staticmethod
#     async def on_after_forgot_password(user: User, token: str):
#         print(f"User {user.id} has forgot their password. Reset token: {token}")
#
#     @staticmethod
#     async def on_after_request_verify(user: User, token: str):
#         print(f"Verification requested for user {user.id}. Verification token: {token}")
#
#     async def create(
#         self,
#         user_create: UserCreateSchema,
#         safe: bool = False,
#     ) -> tuple[dict, dict]:
#         """
#         Create a user in database.
#
#         Triggers the on_after_register handler on success.
#
#         :param user_create: The UserCreateSchema to create.
#         :param safe: If True, sensitive values like is_superuser or is_verified
#         will be ignored during the creation, defaults to False.
#         :raises UserAlreadyExists: A user already exists with the same e-mail.
#         :return: A new user.
#
#         """
#         try:
#             validate_email(user_create.email, timeout=5)
#         except Exception as e:
#             raise AuthApiErrors.REGISTER_INVALID_EMAIL.exception(e)
#
#         if await self._email_exists(user_create.email):
#             raise AuthApiErrors.REGISTER_USER_ALREADY_EXISTS.exception
#
#         user_dict = user_create.create_update_dict() if safe else user_create.create_update_dict_superuser()
#         password = user_dict.pop("password")
#         user_dict["hashed_password"] = self.password_helper.hash(password)
#         nickname = user_dict.get("nickname")
#         user_dict["nickname_number"] = await self.user_db.generate_nickname_number(
#             nickname,
#         )
#
#         created_user = await self.user_db.create(user_dict)
#
#         await self.on_after_register(created_user)
#
#         payload = UserPayload.from_orm(created_user)
#         user_data = jsonable_encoder(payload)
#         tokens = self.jwt_backend.create_tokens(user_data)
#
#         return user_data, tokens
#
#     async def _email_exists(self, email: str) -> bool:
#         return await self.user_db.get_by_email(email) is not None
#
#     async def request_new_password(self, email: str, background_tasks: BackgroundTasks) -> None:
#         if await self.user_db.get_by_email(email):
#             token = await self._create_random_string()
#             token_hash = await self._hash_string(token)
#             new_password = genword(length=14)
#             await self.user_db.request_new_password(email, token_hash, new_password)
#             email_client = create_email_client()
#             background_tasks.add_task(
#                 email_client.send_new_password_email,
#                 EmailSchema(email=[email]),
#                 token,
#                 new_password,
#             )
#
#     @staticmethod
#     async def _create_random_string(length=255) -> str:
#         return genword(length=length)
#
#     @staticmethod
#     async def _hash_string(string: str) -> str:
#         return hashlib.sha256(string.encode()).hexdigest()
#
#     async def confirm_new_password(self, token: str) -> None:
#         token_hash = await self._hash_string(token)
#         user, new_password = await self.user_db.get_confirm_new_password_user(token_hash)
#
#         if user and new_password:
#             hashed_password = self.password_helper.hash(new_password)
#             await self.user_db.set_new_password(user, hashed_password)
#         else:
#             raise AuthApiErrors.REQUEST_NEW_PASSWORD_BAD_TOKEN.exception
#
#         return None
#
#     async def login(self, user_login: UserLoginSchema) -> tuple[dict, dict]:
#         user = await self.user_db.get_by_email(user_login.email)
#         if user is None:
#             raise AuthApiErrors.LOGIN_BAD_CREDENTIALS.exception
#
#         is_valid, needs_update = self.password_helper.verify_and_update(user_login.password, user.hashed_password)
#         if not is_valid:
#             raise AuthApiErrors.LOGIN_BAD_CREDENTIALS.exception
#
#         payload = UserPayload.from_orm(user)
#         user_data = jsonable_encoder(payload)
#         tokens = self.jwt_backend.create_tokens(user_data)
#
#         return user_data, tokens
#
#     async def refresh_access_token(self, refresh_token: str) -> str:
#         refresh_token_payload = await self.jwt_backend.decode_token(refresh_token)
#         if refresh_token_payload is None or refresh_token_payload.get("type") != "refresh":
#             raise AuthApiErrors.INVALID_CREDENTIALS.exception
#
#         user = await self.user_db.get(refresh_token_payload.get("id"))
#         if user is None or not user.is_active:
#             raise AuthApiErrors.INVALID_CREDENTIALS.exception
#
#         payload = UserPayload.from_orm(user)
#         user_data = jsonable_encoder(payload)
#         access_token = self.jwt_backend.create_access_token(user_data)
#
#         return access_token
#
#
# @alru_cache()
# async def get_user_manager() -> UserManager:
#     jwt_backend = await get_jwt_backend()
#     return UserManager(user_db, jwt_backend, password_helper)
