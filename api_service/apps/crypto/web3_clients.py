# -*- coding: utf-8 -*-
from abc import ABC
from datetime import datetime, timedelta
from typing import List

import httpx
from moralis.evm_api import evm_api
from web3 import Web3
from web3.gas_strategies.rpc import rpc_gas_price_strategy

from api_service.apps.crypto.exceptions import InvalidRecipientException, SendTransactionException
from api_service.apps.crypto.models import Wallet
from api_service.apps.crypto.schemas import TransactionCreate
from api_service.apps.crypto.utils.decoders import BaseDecoder
from api_service.config.settings import settings


class BaseClient(ABC):
    endpoint = settings.infura_api_url

    @property
    def client(self):
        return httpx.AsyncClient()

    @property
    def provider(self):
        provider = Web3(Web3.WebsocketProvider(self.endpoint))
        provider.eth.set_gas_price_strategy(rpc_gas_price_strategy)
        return provider

    @staticmethod
    async def send_request(request):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.send(request)
            return response
        except Exception as error:
            raise error

    def from_wei_to_eth(self, value):
        return format(float(self.provider.fromWei(int(value), "ether")), ".8f")


class EthereumProviderClient(BaseClient, BaseDecoder):
    async def get_balance(self, address: str):
        return self.from_wei_to_eth(self.provider.eth.get_balance(address))

    async def get_tx(self, transaction_create: TransactionCreate, wallet: Wallet):
        try:
            tx = self.provider.eth.account.sign_transaction(
                {
                    "nonce": self.provider.eth.get_transaction_count(wallet.address),
                    "gasPrice": self.provider.eth.generate_gas_price(),
                    "gas": 21000,
                    "to": transaction_create.address_to,
                    "value": self.provider.toWei(transaction_create.value, "ether"),
                    "chainId": 11155111,
                },
                wallet.private_key,
            )
        except TypeError:
            raise InvalidRecipientException()
        return tx

    async def send_raw_transaction(self, transaction_create: TransactionCreate, wallet: Wallet) -> str:
        tx = await self.get_tx(transaction_create, wallet)
        try:
            tx_hash = self.provider.eth.send_raw_transaction(tx.rawTransaction)
            tx_receipt = self.provider.eth.wait_for_transaction_receipt(tx_hash)
        except Exception as ex:
            print(f"Web3 got some exception - {str(ex)}")
            raise SendTransactionException(message=str(ex))
        return str(tx_receipt.transactionHash.hex())  # noqa

    async def get_transactions_from_block(self, block_hash, addresses: List[str]):
        try:
            transactions = self.provider.eth.get_block(block_hash, True)["transactions"]
        except Exception:
            return

        if transactions:
            transactions = [
                transaction
                for transaction in transactions
                if transaction["to"] in addresses or transaction["from"] in addresses  # noqa
            ]
            return transactions


class EtherscanClient(BaseClient, BaseDecoder):
    endpoint = settings.etherscan_api_url

    async def get_result(self, data: dict) -> List[dict]:
        transactions = [
            {
                "block_number": transaction.get("blockNumber"),
                "txn_hash": transaction.get("hash")
                if isinstance(transaction.get("hash"), str)
                else transaction.get("hash").hex(),
                "address_from": transaction.get("from"),
                "address_to": transaction.get("to"),
                "value": self.from_wei_to_eth(transaction.get("value")),
                "age": self.timestamp_to_period(transaction.get("timeStamp")),
                "txn_fee": self.from_wei_to_eth(int(transaction.get("gasPrice")) * 21000),
                "status": True
                if transaction.get("txreceipt_status") == "1" or transaction.get("txreceipt_status") is None
                else False,
            }
            for transaction in data.get("result")
        ]
        return transactions

    async def get_result_txn(self, data: dict) -> List[dict]:
        transactions = [
            {
                "block_number": transaction.get("block_number"),
                "txn_hash": transaction.get("hash")
                if isinstance(transaction.get("hash"), str)
                else transaction.get("hash").hex(),
                "address_from": transaction.get("from_address"),
                "address_to": transaction.get("to_address"),
                "value": self.from_wei_to_eth(transaction.get("value")),
                "age": self.str_to_date(transaction.get("block_timestamp")),
                "txn_fee": self.from_wei_to_eth(int(transaction.get("gas_price")) * 21000),
                "status": True
                if transaction.get("receipt_status") == "1" or transaction.get("receipt_status") is None
                else False,
            }
            for transaction in data.get("result")
        ]
        return transactions

    async def get_list_transactions(self, address: str) -> List[dict]:
        api_key = settings.moralis_api_key
        params = {
            "address": address,
            "chain": "sepolia",
            "subdomain": "",
            "from_date": datetime.now() - timedelta(days=60),
            "to_date": datetime.now(),
            "cursor": "",
            "limit": 100,
        }

        result = evm_api.transaction.get_wallet_transactions(
            api_key=api_key,
            params=params,  # noqa
        )
        return await self.get_result_txn(result)
