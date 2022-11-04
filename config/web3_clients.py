# -*- coding: utf-8 -*-
from abc import ABC
from typing import List

import httpx
from web3 import Web3
from web3.gas_strategies.rpc import rpc_gas_price_strategy

from apps.crypto.exceptions import InvalidRecipientException, SendTransactionException
from apps.crypto.models import Wallet
from apps.crypto.schemas import TransactionCreate
from apps.crypto.utils.decoders import BaseDecoder
from config.settings import settings


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
            raise SendTransactionException(message=str(ex))
        return str(tx_receipt.transactionHash.hex())

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

    async def get_list_transactions(self, address: str) -> List[dict]:
        params = {
            "module": "account",
            "action": "txlist",
            "address": address,
            "startblock": 0,
            "endblock": 99999999,
            "page": 1,
            "offset": 100,
            "sort": "asc",
            "apikey": settings.etherscan_api_key,
        }
        request = self.client.build_request(method="GET", url=self.endpoint, params=params)
        response = await self.send_request(request)
        result = response.json()
        return await self.get_result(result)
