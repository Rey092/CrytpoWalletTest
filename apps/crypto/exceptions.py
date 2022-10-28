# -*- coding: utf-8 -*-
from fastapi_helper.exceptions.http_exceptions import DefaultHTTPException
from starlette import status


class WalletAlreadyExistException(DefaultHTTPException):
    code = "private_key_error"
    type = "Wallet Already Exist"
    message = "A wallet with this address already exists for this user."
    status_code = status.HTTP_400_BAD_REQUEST


class InvalidPrivateKeyException(DefaultHTTPException):
    code = "private_key_error"
    type = "Invalid Private Key"
    message = "The private key is invalid."
    status_code = status.HTTP_400_BAD_REQUEST


class InvalidSenderException(DefaultHTTPException):
    code = "address_error"
    type = "Invalid Sender Address"
    message = "Field 'address_from' is invalid."
    status_code = status.HTTP_400_BAD_REQUEST


class InvalidRecipientException(DefaultHTTPException):
    code = "address_error"
    type = "Invalid Recipient Address"
    message = "Field 'address_to' is invalid."
    status_code = status.HTTP_400_BAD_REQUEST


class InvalidValueException(DefaultHTTPException):
    code = "value_error"
    type = "Invalid Value"
    message = "The value is invalid"
    status_code = status.HTTP_400_BAD_REQUEST


class SendTransactionException(DefaultHTTPException):
    code = "transaction_error"
    type = "Send Transaction Error"
    message = "Something wrong..."
    status_code = status.HTTP_400_BAD_REQUEST
