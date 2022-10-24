# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from fastapi_helper.schemas.examples import examples_generate
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from apps.users import crud, schemas
from apps.users.exceptions import (
    EmailAlreadyExistException,
    EmailInvalidException,
    PasswordInvalidException,
    PasswordMismatchException,
    UsernameInvalidException,
)
from apps.users.utils.validators import validate_email_, validate_password, validate_username
from config.db import SessionLocal

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
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserRegisterResponse,
    responses=examples_generate.get_error_responses(
        EmailInvalidException,
        EmailAlreadyExistException,
        PasswordMismatchException,
        PasswordInvalidException,
        UsernameInvalidException,
    ),
)
async def register(user: schemas.UserRegister, db: Session = Depends(get_db)):
    result = await validate_email_(user.email)
    if result.get("email"):
        if crud.get_user_by_email(db, email=user.email):
            raise EmailAlreadyExistException()
    else:
        raise EmailInvalidException(message=result.get("message"))

    if not await validate_password(user.password1):
        raise PasswordInvalidException()
    if user.password1 != user.password2:
        raise PasswordMismatchException()

    if not await validate_username(user.username):
        raise UsernameInvalidException()

    return crud.create_user(db=db, user=user)
