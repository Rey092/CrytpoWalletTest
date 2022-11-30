# -*- coding: utf-8 -*-
from fastapi_helper.utilities.password_helper import PasswordHelper
from sqlalchemy.orm import Session

from api_service.apps.users.models import Permission, User
from api_service.config.settings import settings

password_helper = PasswordHelper()


def create_user(db: Session):
    if not db.query(User).all():
        db_user = User(
            username=settings.username,
            email=settings.user_email,
            password=password_helper.hash(settings.user_password),
        )
        db.add(db_user)
        db.commit()
        db_permission = Permission(
            has_access_chat=True,
            user_id=db_user.id,
        )
        db.add(db_permission)
        db.commit()
