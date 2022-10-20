# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session

from apps.users.models import User
from apps.users.schemas import UserRegister
from config.utils.password_helper import password_helper


def create_user(db: Session, user: UserRegister):
    fake_hashed_password = password_helper.hash(user.password1)
    db_user = User(email=user.email, username=user.username, password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
