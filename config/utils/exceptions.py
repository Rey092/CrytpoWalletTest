# -*- coding: utf-8 -*-
from fastapi_helper.exceptions.http_exceptions import DefaultHTTPException
from starlette import status


class AuthEmailException(DefaultHTTPException):
    code = "email_error"
    type = "Email Error"
    message = "Email already registered."
    status_code = status.HTTP_400_BAD_REQUEST

    def example(self):
        example = {
            "summary": self.type,
            "value": {
                "detail": [
                    {
                        "code": self.code,
                        "type": self.type,
                        "message": self.message,
                    },
                ],
            },
        }
        return example


class AuthPasswordMismatchException(DefaultHTTPException):
    code = "password_mismatch_error"
    type = "Password Mismatch Error"
    message = "Password mismatch."
    status_code = status.HTTP_400_BAD_REQUEST

    def example(self):
        example = {
            "summary": self.type,
            "value": {
                "detail": [
                    {
                        "code": self.code,
                        "type": self.type,
                        "message": self.message,
                    },
                ],
            },
        }
        return example
