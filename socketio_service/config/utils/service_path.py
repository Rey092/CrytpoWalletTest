# -*- coding: utf-8 -*-
import yarl


async def get_path(data):
    try:
        url = data.get("HTTP_REFERER")
        return True if yarl.URL(url).path_qs == "/chat/messages" else False
    except Exception as ex:
        print(ex)
        return False
