# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from apps.users import crud, schemas
from config.db import SessionLocal
from config.utils.examples_gen import error_responses
from config.utils.exceptions import AuthEmailException, AuthPasswordMismatchException

auth_router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class User(BaseModel):
    email: str
    password: str


@auth_router.post("/login")
async def login(user: User):
    return user


@auth_router.post(
    "/register",
    response_model=schemas.UserResponse,
    responses=error_responses(AuthEmailException(), AuthPasswordMismatchException()),
)
def create_user(user: schemas.UserRegister, db: Session = Depends(get_db)):
    if user.password1 != user.password2:
        raise AuthPasswordMismatchException()
    user_db = crud.get_user_by_email(db, email=user.email)
    if user_db:
        raise AuthEmailException()
    return crud.create_user(db=db, user=user)
