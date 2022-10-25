# -*- coding: utf-8 -*-
"""
FastAPI Users database adapter for SQLAlchemy ORM.
"""
import random
from typing import Type, TypeVar

from pydantic import UUID4

from apps.users.models import Permission, User
from apps.users.schemas import UserRegister
from config.db import SessionLocal

# from fastapi_users.db import BaseUserDatabase


UD = TypeVar("UD")


class UserDatabase:
    """
    Database adapter for SQLAlchemy ORM.

    :param user_model: user model.

    """

    model: Type[User]

    def __init__(self, user_model: Type[User], permission_model: Type[Permission]):
        self.model = user_model
        self.permission = permission_model
        self.db = SessionLocal()

    async def get(self, id: UUID4) -> User:
        return self.db.query(self.model).filter(self.model.id == id).first()

    async def get_user_by_email(self, email: str) -> User:
        return self.db.query(self.model).filter(self.model.email == email).first()

    async def create(self, user: UserRegister) -> User:
        db_user = self.model(email=user.email, username=user.username, password=user.password1)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        await self.create_user_permission(db_user.id)
        return db_user

    async def create_user_permission(self, user_id: UUID4) -> Permission:
        db_permission = self.permission(has_access_chat=False, user_id=user_id)
        self.db.add(db_permission)
        self.db.commit()
        self.db.refresh(db_permission)
        return db_permission

    async def generate_nickname_number(self, nickname: str) -> str:
        query = self.model.filter(nickname__iexact=nickname).values("nickname_number")
        nickname_numbers = list(await query)
        while True:
            nickname_number = random.randint(0, 9999)
            if nickname_number not in nickname_numbers:
                break
        return str(nickname_number).zfill(4)

    async def update(self, user: UD) -> UD:
        raise NotImplementedError
        # user_dict = user.dict()
        # user_dict.pop("id")  # Tortoise complains if we pass the PK again
        # oauth_accounts = user_dict.pop("oauth_accounts", None)
        #
        # model = await self.model.get(id=user.id)
        # for field in user_dict:
        #     setattr(model, field, user_dict[field])
        # await model.save()
        #
        # if oauth_accounts and self.oauth_account_model:
        #     await model.oauth_accounts.all().delete()  # type: ignore
        #     oauth_account_objects = []
        #     for oauth_account in oauth_accounts:
        #         oauth_account_objects.append(
        #             self.oauth_account_model(user=model, **oauth_account),
        #         )
        #     await self.oauth_account_model.bulk_create(oauth_account_objects)
        #
        # return user

    async def delete(self, user: UD) -> None:
        await self.model.filter(id=user.id).delete()

    # async def request_new_password(self, email: str, token_hash: str, new_password: str) -> str:
    #     new_password_token, created = await self.new_password_token_model.request_new_password(
    #         email=email,
    #         token_hash=token_hash,
    #         new_password=new_password,
    #     )
    #     return new_password_token.new_password

    # async def get_confirm_new_password_user(self, token_hash: str) -> Tuple[Optional[User], Optional[str]]:
    #     query = self.new_password_token_model.filter(token_hash=token_hash)
    #     new_password_token = await query.first()
    #
    #     if new_password_token:
    #         email = new_password_token.email
    #         user = await self.model.filter(email=email).first()
    #         await new_password_token.delete()
    #         return user, new_password_token.new_password
    #
    #     else:
    #         return None, None

    @staticmethod
    async def set_new_password(user: User, new_password: str) -> None:
        user.hashed_password = new_password
        await user.save()
