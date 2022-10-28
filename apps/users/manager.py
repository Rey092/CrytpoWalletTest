# -*- coding: utf-8 -*-
from typing import Tuple

from fastapi.encoders import jsonable_encoder
from fastapi_helper.exceptions.auth_http_exceptions import InvalidCredentialsException
from pydantic import UUID4
from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks

from config.utils.email_client import EmailSchema, create_email_client
from config.utils.password_helper import PasswordHelper

from .database import UserDatabase
from .exceptions import (
    EmailAlreadyExistException,
    EmailInvalidException,
    PasswordInvalidException,
    PasswordMismatchException,
    UsernameInvalidException,
)
from .jwt_backend import JWTBackend
from .schemas import UserLogin, UserRegister
from .utils.validators import validate_email_, validate_password, validate_username


class UserManager:
    def __init__(
        self,
        database: UserDatabase,
        jwt_backend: JWTBackend,
        pass_helper: PasswordHelper,
    ):
        self.user_db = database
        self.jwt_backend = jwt_backend
        self.password_helper = pass_helper

    async def get_user(self, user_id: UUID4, db: Session):
        """

        :param user_id:
        :param db:
        :return:
        """
        user = await self.user_db.get(user_id, db)
        return user

    async def create(
        self,
        user_create: UserRegister,
        db: Session,
        background_tasks: BackgroundTasks,
    ) -> Tuple[dict, str]:
        """

        :param user_create:
        :param db:
        :param background_tasks:
        :return:
        """
        result = await validate_email_(user_create.email)
        if result.get("email"):
            if await self.user_db.get_user_by_email(email=user_create.email, db=db):
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
        created_user = await self.user_db.create(user_create, db=db)
        payload = {
            "id": str(created_user.id),
            "username": created_user.username,
            "avatar": created_user.avatar,
        }
        access_token = self.jwt_backend.create_access_token(payload)
        email_client = create_email_client()
        background_tasks.add_task(
            email_client.send_email_to_new_user,
            EmailSchema(
                email=created_user.email,
                username=created_user.username,
            ),
        )
        return payload, access_token

    async def login(self, user_login: UserLogin, db: Session) -> Tuple[dict, str]:
        """

        :param user_login:
        :param db:
        :return:
        """
        user = await self.user_db.get_user_by_email(email=user_login.email, db=db)
        if user is None:
            raise InvalidCredentialsException()
        is_valid, needs_update = self.password_helper.verify_and_update(user_login.password, user.password)
        if not is_valid:
            raise InvalidCredentialsException()
        user_data = jsonable_encoder(user)
        access_token = self.jwt_backend.create_access_token(user_data)
        return user_data, access_token

    async def update_permission(self, user_id: UUID4, db: Session):
        """

        :param user_id:
        :param db:
        :return:
        """
        await self.user_db.change_access_chat_permission(user_id, db)
