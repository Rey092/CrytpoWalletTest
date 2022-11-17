# -*- coding: utf-8 -*-


async def get_path(data):
    try:
        path = data.get("path")
        return True if path == "/chat/messages" else False
    except Exception as ex:
        print(ex)
        return False
