# -*- coding: utf-8 -*-
import asyncio
import logging
from threading import Thread

from api_service.apps.crypto.dependencies import get_api_service_producer, get_ethereum_manager
from api_service.config.db import SessionLocal

logger = logging.getLogger(__name__)


async def parsing_balance():
    db = SessionLocal()
    ethereum_manager = await get_ethereum_manager()
    producer = await get_api_service_producer()

    logger.info("[*] Wallets balance parser started")

    while True:
        await asyncio.sleep(120)
        wallets = await ethereum_manager.get_all_wallets(db)
        wallets_for_update = []

        for wallet in wallets:
            balance = await ethereum_manager.parse_wallet_balance(wallet.address)
            if float(balance) != float(wallet.balance):
                wallet.balance = balance
                wallets_for_update.append(wallet)
                await producer.publish_message(
                    exchange_name="wallet_balance_exchange",
                    message={"wallet_address": str(wallet.address), "value": balance},
                )
        await ethereum_manager.update_wallets_balances(db, wallets_for_update)


parsing_balances_thread = Thread(target=asyncio.run, args=(parsing_balance(),))
