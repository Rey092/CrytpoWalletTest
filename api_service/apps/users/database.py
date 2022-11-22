# -*- coding: utf-8 -*-
"""
FastAPI Users database adapter for SQLAlchemy ORM.
"""
from typing import Type, TypeVar
from uuid import UUID

from sqlalchemy.orm import Session

from api_service.apps.users.models import Permission, User
from api_service.apps.users.schemas import UserRegister, UserUpdate

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

    async def change_access_chat_permission(self, user_id: UUID, db: Session) -> None:
        db.query(self.permission).filter(self.permission.user_id == user_id).update({"has_access_chat": True})
        db.commit()

    async def change_count_messages(self, user_id, count, db: Session) -> None:
        db.query(self.model).filter(self.model.id == user_id).update({"count_messages": count})
        db.commit()

    async def update(self, user_id: UUID, user_data: UserUpdate, db: Session) -> User:
        user = db.query(self.model).filter(self.model.id == user_id)
        if user_data.password:
            await self.new_password(user_id, user_data.password, db)
        if user_data.delete is True or user_data.profile_image is not None:
            user.update({"username": user_data.username, "avatar": user_data.profile_image})
        else:
            user.update({"username": user_data.username})
        db.commit()
        return user.first()

    async def new_password(self, user_id: UUID, password, db: Session) -> None:
        db.query(self.model).filter(self.model.id == user_id).update(
            {"password": password},
        )
        db.commit()
