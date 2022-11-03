# -*- coding: utf-8 -*-
"""
FastAPI Users database adapter for SQLAlchemy ORM.
"""
from typing import Type, TypeVar
from uuid import UUID

from sqlalchemy.orm import Session

from apps.users.models import Permission, User
from apps.users.schemas import UserRegister, UserUpdate

UD = TypeVar("UD")


class UserDatabase:
    """

    :param user_model: user model.
    :param permission_model: permission_model

    """

    model: Type[User]

    def __init__(self, user_model: Type[User], permission_model: Type[Permission]):
        self.model = user_model
        self.permission = permission_model

    async def get(self, user_id: UUID, db: Session) -> User:
        return db.query(self.model).filter(self.model.id == user_id).first()

    async def get_user_by_email(self, email: str, db: Session) -> User:
        return db.query(self.model).filter(self.model.email == email).first()

    async def create(self, user: UserRegister, db: Session) -> User:
        db_user = self.model(email=user.email, username=user.username, password=user.password1)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        await self.create_user_permission(db_user.id, db)
        return db.query(self.model).filter(self.model.email == db_user.email).first()

    async def create_user_permission(self, user_id: UUID, db: Session) -> Permission:
        db_permission = self.permission(has_access_chat=False, user_id=user_id)
        db.add(db_permission)
        db.commit()
        db.refresh(db_permission)
        return db_permission

    async def change_access_chat_permission(self, user_id: UUID, db: Session):
        db.query(self.permission).filter(self.permission.user_id == user_id).update({"has_access_chat": True})
        db.commit()

    async def update(self, user_id: UUID, user_data: UserUpdate, db: Session):

        db.query(self.model).filter(self.model.id == user_id).update(
            {"username": user_data.username, "avatar": user_data.profile_image},
        )
        db.commit()
        return db.query(self.model).filter(self.model.id == user_id).first()

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
