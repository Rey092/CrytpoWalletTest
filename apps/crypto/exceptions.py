# -*- coding: utf-8 -*-
from fastapi_helper.exceptions.http_exceptions import DefaultHTTPException
from starlette import status


class WalletAlreadyExistException(DefaultHTTPException):
    code = "private_key_error"
    type = "Wallet Already Exist"
    message = "A wallet with this address already exists for this user."
    status_code = status.HTTP_400_BAD_REQUEST
