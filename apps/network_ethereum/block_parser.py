# -*- coding: utf-8 -*-
# import asyncio
# import json
#
# import httpx
# from web3 import Web3
# from websockets import connect
#
# infura_ws_url = "wss://sepolia.infura.io/ws/v3/7c8d5f115738446d9bf671107b64c3a7"
# w3 = Web3(Web3.WebsocketProvider(infura_ws_url))
#
#
# async def get_event():
#     async with connect(infura_ws_url) as websocket:
#         await websocket.send(
#             '{"jsonrpc": "2.0", "id": 1, "method": "eth_subscribe", "params": ["newHeads"]}',
#         )
#         subscription_response = await websocket.recv()
#         print(subscription_response)
#         while True:
#             try:
#                 message = await asyncio.wait_for(websocket.recv(), timeout=2)
#                 response = json.loads(message)
#                 block_number = response["params"]["result"]["number"]
#                 await get_transactions_by_block(block_number)
#             except:
#                 pass
#
#
# def get_transaction():
#     url = "https://eth.getblock.io/sepolia/?api_key=96057970-171d-440d-a450-c5b0053600b3"
#     with httpx.Client() as client:
#         json = {
#             "jsonrpc": "2.0",
#             "method": "eth_getBlockByHash",
#             "params": ["0x28576d589227244fd15b86296d63a905e4033b8da3808bef81ce64bf011f453a", True],
#             "id": "etblock.io",
#         }
#         response = client.post(url, json=json)
#     return response.text
#
#
# async def get_transactions_by_block(block_hash):
#     try:
#         transactions = w3.eth.get_block(block_hash, True)["transactions"]
#     except:
#         print("Возникла какая-то ошибка...")
#         return
#
#     if transactions:
#         for transaction in transactions:
#             print(f'Address from: {transaction["from"]}')
#             print(f'Address to: {transaction["to"]}')
#             if (
#                 transaction["to"] == "0x71Df913fab8083A7ed2529fd02eebEcB066E7549"
#                 or transaction["from"] == "0x71Df913fab8083A7ed2529fd02eebEcB066E7549"
#             ):
#                 print(f'Ура, есть совпадение! Вот нужная транзакция: {transaction.get("hash").hex()}')
#             else:
#                 print("Совпадений нет =(")
#             print("------------------------------------------------------------")
#     else:
#         print("Транзакций в блоке нет!")
#
#
# if __name__ == "__main__":
#     asyncio.run(get_event())
