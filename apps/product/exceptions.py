# -*- coding: utf-8 -*-
from fastapi_helper.exceptions.http_exceptions import DefaultHTTPException
from starlette import status


class InvalidPriceException(DefaultHTTPException):
    code = "price_error"
    type = "Invalid Price"
    message = "Price must be greater than zero."
    status_code = status.HTTP_400_BAD_REQUEST


class InvalidWalletException(DefaultHTTPException):
    code = "wallet_error"
    type = "Invalid Wallet ID"
    message = "Wallet id is invalid."
    status_code = status.HTTP_400_BAD_REQUEST
