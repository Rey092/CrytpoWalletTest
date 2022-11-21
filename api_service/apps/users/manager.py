# -*- coding: utf-8 -*-
from typing import Tuple
from uuid import UUID

from aio_pika import ExchangeType
from fastapi_helper.exceptions.auth_http_exceptions import InvalidCredentialsException
from fastapi_helper.utilities.password_helper import PasswordHelper
from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks

from api_service.config.settings import settings
from api_service.config.storage import SqlAlchemyStorage
from api_service.config.utils.email_client import EmailSchema, create_email_client

from ...api_service_producer import ApiServiceProducer
from .database import UserDatabase
from .exceptions import (
    DeleteImageInvalidException,
    DeleteNotImageInvalidException,
    EmailAlreadyExistException,
    EmailInvalidException,
    PasswordInvalidException,
    PasswordMismatchException,
    UsernameInvalidException,
)
from .jwt_backend import JWTBackend
from .schemas import UserLogin, UserRegister, UserUpdate
from .utils.decoder import timestamp_to_period
from .utils.validators import validate_email_, validate_password, validate_username


class UserManager:
    def __init__(
        self,
        database: UserDatabase,
        jwt_backend: JWTBackend,
        pass_helper: PasswordHelper,
        storage: SqlAlchemyStorage,
        producer: ApiServiceProducer,
    ):
        self.user_db = database
        self.jwt_backend = jwt_backend
        self.password_helper = pass_helper
        self.storage = storage
        self.producer = producer

    @staticmethod
    async def get_payload(user_data):
        """
        :param user_data:
        :return: payload:
        """
        payload = {
            "id": str(user_data.id),
            "username": user_data.username,
            "avatar": user_data.avatar,
        }
        return payload

    async def get_user(self, user_id: UUID, db: Session):
        """
        :param user_id:
        :param db:
        :return: User:
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
        :return: payload and access_token:
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
        payload = await self.get_payload(created_user)
        await self.producer.publish_message(
            exchange_name="user_topic_exchange",
            message=payload,
            routing_key="id.username.avatar.create",
            exchange_type=ExchangeType.TOPIC,
        )
        access_token = self.jwt_backend.create_access_token(payload, False)
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
        :return: user data and access token:
        """
        user = await self.user_db.get_user_by_email(email=user_login.email, db=db)
        if user is None:
            raise InvalidCredentialsException()
        is_valid, needs_update = self.password_helper.verify_and_update(user_login.password, user.password)
        if not is_valid:
            raise InvalidCredentialsException()
        payload = await self.get_payload(user)
        access_token = self.jwt_backend.create_access_token(payload, user_login.remember_me)
        return payload, access_token

    async def update(
        self,
        user_id: UUID,
        user_token: str,
        user_data: UserUpdate,
        db: Session,
    ):
        """

        :param user_id:
        :param user_token:
        :param user_data:
        :param db:
        :return:
        """
        if not await validate_username(user_data.username):
            raise UsernameInvalidException()
        if user_data.password or user_data.repeat_password:
            if user_data.password != user_data.repeat_password:
                raise PasswordMismatchException()
            else:
                if not await validate_password(user_data.password):
                    raise PasswordInvalidException()
                else:
                    user_data.password = self.password_helper.hash(user_data.password)
        if user_data.profile_image and user_data.delete is True:
            raise DeleteImageInvalidException()
        user = await self.user_db.get(user_id, db)
        if user_data.profile_image is not None:
            path = await self.storage.upload(
                file=user_data.profile_image,
                upload_to="profile",
                sizes=(100, 100),
                content_types=["png", "jpg", "jpeg"],
            )
            user_data.profile_image = path
            if user.avatar is not None:
                await self.storage.delete(user.avatar)
        if user_data.delete is True:
            if user.avatar is None:
                raise DeleteNotImageInvalidException()
            else:
                await self.storage.delete(user.avatar)
        user = await self.user_db.update(
            user_id=user_id,
            user_data=user_data,
            db=db,
        )
        payload = await self.get_payload(user)
        await self.producer.publish_message(
            exchange_name="user_topic_exchange",
            message=payload,
            routing_key="id.username.avatar.update",
            exchange_type=ExchangeType.TOPIC,
        )
        old_token = await self.jwt_backend.decode_token(user_token)
        access_token = self.jwt_backend.create_access_token(payload, False)
        if timestamp_to_period(old_token.get("iat"), old_token.get("exp")) == settings.jwt_access_not_expiration:
            access_token = self.jwt_backend.create_access_token(payload, True)
        return user, access_token

    async def update_permission(self, user_id: UUID, db: Session):
        """
        :param user_id:
        :param db:
        :return: None
        """
        message = {
            "user_id": user_id,
        }
        await self.user_db.change_access_chat_permission(user_id, db)
        await self.producer.publish_message(
            exchange_name="update_permission_exchange",
            message=message,
        )

    async def update_count_message(
        self,
        db: Session,
        data,
    ):
        """

        :param data:
        :param db:
        :return: None
        """
        user_id: UUID = UUID(data.get("user_id"))
        count: int = data.get("count")
        await self.user_db.change_count_messages(
            user_id,
            count,
            db,
        )
