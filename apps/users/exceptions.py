# -*- coding: utf-8 -*-
from fastapi_helper.exceptions.http_exceptions import DefaultHTTPException
from starlette import status


class EmailInvalidException(DefaultHTTPException):
    code = "email_error"
    type = "Email Invalid"
    message = "The email address is not valid."
    status_code = status.HTTP_400_BAD_REQUEST


class EmailAlreadyExistException(DefaultHTTPException):
    code = "email_error"
    type = "Email Already Exist Error"
    message = "Email already registered."
    status_code = status.HTTP_400_BAD_REQUEST


class PasswordInvalidException(DefaultHTTPException):
    code = "password_error"
    type = "Password Invalid"
    message = (
        "Password must contain at least: one digit, one uppercase letter, one lowercase letter,"
        " one special character[$@#], 8 to 20 characters"
    )
    status_code = status.HTTP_400_BAD_REQUEST


class PasswordMismatchException(DefaultHTTPException):
    code = "password_error"
    type = "Password Mismatch Error"
    message = "Password mismatch."
    status_code = status.HTTP_400_BAD_REQUEST


class UsernameInvalidException(DefaultHTTPException):
    code = "username_error"
    type = "Username Invalid"
    message = "Username must contain at least: 5 to 40 characters, not special characters"
    status_code = status.HTTP_400_BAD_REQUEST
