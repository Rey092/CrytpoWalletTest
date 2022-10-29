# -*- coding: utf-8 -*-
from decimal import Decimal
from uuid import UUID

from fastapi_helper.schemas.camel_schema import ApiSchema


class AssetCreate(ApiSchema):
    id: UUID
    code: str
    network: str
    type: str
    standard: str = None
    decimals: int
    is_currency: bool


# region Wallets
class Wallet(ApiSchema):
    id: UUID
    address: str
    balance: float


class WalletCreate(ApiSchema):
    private_key: str = None
    address: str = None
    user_id: str
    balance: float = 0


class WalletImport(ApiSchema):
    private_key: str


class WalletCreateResponse(ApiSchema):
    address: str
    message: str = "The new wallet has been successfully created."


class WalletImportResponse(WalletCreateResponse):
    address: str
    message: str = "The wallet has been successfully imported."


# endregion Wallets


# region Transactions
class Transaction(ApiSchema):
    txn_hash: str
    address_from: str
    address_to: str
    value: float
    age: int
    txn_fee: Decimal
    status: bool


class TransactionCreate(ApiSchema):
    address_from: str
    address_to: str
    value: float


class TransactionCreateResponse(ApiSchema):
    txn_hash: str
    message: str = "Transaction sent successfully."


# endregion Transactions
