# -*- coding: utf-8 -*-
import asyncio
import datetime
from threading import Thread

import aiohttp

COUNT_FAILED = 0


async def send(session):
    try:
        resp = await session.get(url="https://www.google.com/")
    except Exception:
        global COUNT_FAILED
        COUNT_FAILED += 1
        return
    return resp.status


async def main(requests):
    async with aiohttp.ClientSession() as session:
        tasks = [send(session) for _ in range(requests)]
        start = datetime.datetime.now()
        results = await asyncio.gather(*tasks)
        print(datetime.datetime.now() - start)
        return results


async def send_requests():
    global COUNT_FAILED
    COUNT_FAILED = 0

    threads = [Thread(target=asyncio.run, args=(main(1667),)) for _ in range(6)]
    try:
        print("sending 10 000 requests")
        [thread.start() for thread in threads]
    except Exception as ex:
        print(f"Something went wrong - {str(ex)}")
        return False
    [thread.join() for thread in threads]

    if COUNT_FAILED == 0:
        print("OK")
        return True
    else:
        print("NOT OK")
        return False
