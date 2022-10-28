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
#             except Exception:
#                 pass
#
#
# if __name__ == "__main__":
#     asyncio.run(get_event())
