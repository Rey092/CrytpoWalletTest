# -*- coding: utf-8 -*-
from apps.socketio_app.models import ChatMessage


class ChatDatabase:
    """
    Chat database adapter for ChatMessage and ChatUser.
    """

    @staticmethod
    async def create_message(
        new_message: ChatMessage,
    ):
        message = await new_message.create()
        print(message)
