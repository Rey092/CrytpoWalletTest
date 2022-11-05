# -*- coding: utf-8 -*-
import asyncio
import logging
from threading import Thread

from apps.crypto.dependencies import get_ethereum_manager
from config.db import SessionLocal

logger = logging.getLogger(__name__)


async def parsing_balance():
    db = SessionLocal()
    ethereum_manager = await get_ethereum_manager()

    while True:
        await asyncio.sleep(10)
        wallets = await ethereum_manager.get_all_wallets(db)
        wallets_for_update = []

        for wallet in wallets:
            balance = await ethereum_manager.parse_wallet_balance(wallet.address)
            if float(balance) != float(wallet.balance):
                print(f"Change balance from {wallet.balance} to {balance}")
                wallet.balance = balance
                wallets_for_update.append(wallet)
            else:
                print("balance OK")
        await ethereum_manager.update_wallets_balances(db, wallets_for_update)


parsing_balances_thread = Thread(target=asyncio.run, args=(parsing_balance(),))