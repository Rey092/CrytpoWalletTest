# -*- coding: utf-8 -*-
from fastapi_helper.exceptions.auth_http_exceptions import InvalidCredentialsException
from pydantic import UUID4

# from config.utils import EmailSchema
# from config.utils.email_client import create_email_client
from config.utils.password_helper import PasswordHelper

from .database import UserDatabase

# from .jwt_backend import JWTBackend, get_jwt_backend
from .exceptions import (
    EmailAlreadyExistException,
    EmailInvalidException,
    PasswordInvalidException,
    PasswordMismatchException,
    UsernameInvalidException,
)
from .models import Permission, User
from .schemas import UserLogin, UserRegister
from .utils.validators import validate_email_, validate_password, validate_username

user_db = UserDatabase(User, Permission)


class UserManager:
    def __init__(
        self,
        database: UserDatabase,
        pass_helper: PasswordHelper,
    ):
        self.user_db = database
        self.password_helper = pass_helper

    @staticmethod
    async def on_after_register(user: User):
        """

        :param user: User
        :return: print user id
        """
        print(f"User {user.id} has registered.")

    async def get_user(self, id: UUID4):
        """

        :param id: UUID4
        :return: user
        """
        user = await self.user_db.get(id)
        return user

    async def create(
        self,
        user_create: UserRegister,
        safe: bool = False,
    ) -> tuple[dict, dict]:
        """
        Create a user in database.

        Triggers the on_after_register handler on success.

        :param user_create: The UserCreateSchema to create.
        :param safe: If True, sensitive values like is_superuser or is_verified
        will be ignored during the creation, defaults to False.
        :raises UserAlreadyExists: A user already exists with the same e-mail.
        :return: A new user.

        """
        result = await validate_email_(user_create.email)
        if result.get("email"):
            if await self.user_db.get_user_by_email(email=user_create.email):
                raise EmailAlreadyExistException()
        else:
            raise EmailInvalidException(message=result.get("message"))
        if not await validate_password(user_create.password1):
            raise PasswordInvalidException()
        if user_create.password1 != user_create.password2:
            raise PasswordMismatchException()
        if not await validate_username(user_create.username):
            raise UsernameInvalidException()

        user_create.password1 = self.password_helper.hash(user_create.password1)

        created_user = await self.user_db.create(user_create)

        await self.on_after_register(created_user)

        # payload = UserPayload.from_orm(created_user)
        # user_data = jsonable_encoder(payload)
        # tokens = self.jwt_backend.create_tokens(user_data)

        return created_user

    async def login(self, user_login: UserLogin) -> tuple[dict, dict]:
        """

        :param user_login:
        :return: User
        """
        user = await self.user_db.get_user_by_email(email=user_login.email)
        if user is None:
            raise InvalidCredentialsException()

        is_valid, needs_update = self.password_helper.verify_and_update(user_login.password, user.password)
        if not is_valid:
            raise InvalidCredentialsException()

        # payload = UserPayload.from_orm(user)
        # user_data = jsonable_encoder(payload)
        # tokens = self.jwt_backend.create_tokens(user_data)

        return user

    # async def refresh_access_token(self, refresh_token: str) -> str:
    #     refresh_token_payload = await self.jwt_backend.decode_token(refresh_token)
    #     if refresh_token_payload is None or refresh_token_payload.get("type") != "refresh":
    #         raise AuthApiErrors.INVALID_CREDENTIALS.exception
    #
    #     user = await self.user_db.get(refresh_token_payload.get("id"))
    #     if user is None or not user.is_active:
    #         raise AuthApiErrors.INVALID_CREDENTIALS.exception
    #
    #     payload = UserPayload.from_orm(user)
    #     user_data = jsonable_encoder(payload)
    #     access_token = self.jwt_backend.create_access_token(user_data)
    #
    #     return access_token
