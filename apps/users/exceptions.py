# -*- coding: utf-8 -*-
from fastapi_helper.exceptions.http_exceptions import DefaultHTTPException
from starlette import status


class UnauthorizedException(DefaultHTTPException):
    code = "bearer-001"
    type = "UNAUTHORIZED"
    message = "Credentials were not provided."
    status_code = status.HTTP_401_UNAUTHORIZED


class InvalidCredentialsException(DefaultHTTPException):
    code = "bearer-002"
    type = "LOGIN_BAD_CREDENTIALS"
    message = "Invalid credentials."
    status_code = status.HTTP_401_UNAUTHORIZED


class BadCredentialsException(DefaultHTTPException):
    code = "auth-003"
    type = "INVALID_CREDENTIALS"
    message = "Invalid email or password."
    status_code = status.HTTP_401_UNAUTHORIZED


class InsufficientRightsException(DefaultHTTPException):
    code = "auth-004"
    type = "INSUFFICIENT_RIGHTS"
    message = "Insufficient rights to perform this action."
    status_code = status.HTTP_403_FORBIDDEN


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
