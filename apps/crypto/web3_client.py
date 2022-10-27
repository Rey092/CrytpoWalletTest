# -*- coding: utf-8 -*-
from abc import ABC
from typing import List

import httpx
from web3 import Web3

from apps.crypto.utils.decoders import BaseDecoder


class BaseClient(ABC):
    endpoint = "https://sepolia.infura.io/v3/7c8d5f115738446d9bf671107b64c3a7"

    @property
    def client(self):
        return httpx.AsyncClient()

    @property
    def provider(self):
        return Web3(Web3.HTTPProvider(self.endpoint))

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


class InfuraClient(BaseClient, BaseDecoder):
    async def get_balance(self, address: str):
        return self.from_wei_to_eth(self.provider.eth.get_balance(address))


class EtherscanClient(BaseClient, BaseDecoder):
    endpoint = "https://api-sepolia.etherscan.io/api/"

    async def get_result(self, data: dict) -> List[dict]:
        transactions = [
            {
                "block_number": transaction.get("blockNumber"),
                "txn_hash": transaction.get("hash"),
                "address_from": transaction.get("from"),
                "address_to": transaction.get("to"),
                "value": self.from_wei_to_eth(transaction.get("value")),
                "age": self.timestamp_to_period(transaction.get("timeStamp")),
                "txn_fee": self.from_wei_to_eth(int(transaction.get("gasPrice")) * int(transaction.get("gasUsed"))),
                "status": True if int(transaction.get("txreceipt_status")) == 1 else False,
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
            "apikey": "31AHFCVRWK7WF866J4V4XCHZ59FVCR7HUN",
        }
        request = self.client.build_request(method="GET", url=self.endpoint, params=params)
        response = await self.send_request(request)
        result = response.json()
        return await self.get_result(result)


if __name__ == "__main__":
    # infura_client = InfuraClient()
    # print(infura_client.get_balance())

    eth_client = EtherscanClient()
    print(eth_client.get_list_transactions("0x71Df913fab8083A7ed2529fd02eebEcB066E7549"))
