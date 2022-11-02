# -*- coding: utf-8 -*-
from typing import Tuple, Union
from uuid import UUID

from fastapi import UploadFile
from fastapi_helper.exceptions.auth_http_exceptions import InvalidCredentialsException
from fastapi_helper.utilities.password_helper import PasswordHelper
from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks

from config.storage import SqlAlchemyStorage
from config.utils.email_client import EmailSchema, create_email_client

from .database import UserDatabase
from .exceptions import (
    EmailAlreadyExistException,
    EmailInvalidException,
    PasswordInvalidException,
    PasswordMismatchException,
    UsernameInvalidException,
)
from .jwt_backend import JWTBackend
from .schemas import UserLogin, UserRegister, UserUpdate
from .utils.validators import validate_email_, validate_password, validate_username


class UserManager:
    def __init__(
        self,
        database: UserDatabase,
        jwt_backend: JWTBackend,
        pass_helper: PasswordHelper,
        storage: SqlAlchemyStorage,
    ):
        self.user_db = database
        self.jwt_backend = jwt_backend
        self.password_helper = pass_helper
        self.storage = storage

    async def get_user(self, user_id: UUID, db: Session):
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
        :return: user data and access token
        """
        user = await self.user_db.get_user_by_email(email=user_login.email, db=db)
        if user is None:
            raise InvalidCredentialsException()
        is_valid, needs_update = self.password_helper.verify_and_update(user_login.password, user.password)
        if not is_valid:
            raise InvalidCredentialsException()
        payload = {
            "id": str(user.id),
            "username": user.username,
            "avatar": user.avatar,
        }
        access_token = self.jwt_backend.create_access_token(payload)
        return payload, access_token

    async def update(
        self,
        user_id: UUID,
        user_data: UserUpdate,
        db: Session,
        profile_image: Union[UploadFile, None] = None,
    ):
        """

        :param user_id:
        :param user_data:
        :param db:
        :param profile_image:
        :return:
        """
        profile_image = user_data.profile_image
        if profile_image:
            a = await self.storage.get_image(profile_image)
            print(a)

        user = await self.user_db.update(
            user_id=user_id,
            user_data=user_data,
            db=db,
        )

        return user

    async def update_permission(self, user_id: UUID, db: Session):
        """

        :param user_id:
        :param db:
        :return:
        """
        await self.user_db.change_access_chat_permission(user_id, db)
