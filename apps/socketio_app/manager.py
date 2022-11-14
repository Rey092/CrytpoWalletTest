# -*- coding: utf-8 -*-
from uuid import UUID

from apps.socketio_app.database import ChatDatabase
from apps.socketio_app.models import ChatMessage, ChatUser


class ChatManager:
    def __init__(
        self,
        database: ChatDatabase,
    ):
        self.database = database

    async def new_message(self, message: ChatMessage) -> None:
        await self.database.create_message(message)

    async def get_user(self, user_id: UUID):
        return await self.database.get_user(user_id)

    async def create_user(self, user: ChatUser):
        await self.database.create_user(user)

    async def get_history_chat(self):
        history = []
        list_messages = await self.database.list_message()
        for message in list_messages:
            user = await self.get_user(message.user_id)
            history.append(
                {
                    "message": message.message,
                    "image": message.image,
                    "date": message.date.strftime("%d-%m, %H:%M"),
                    "user_id": str(user.id),
                    "username": user.username,
                    "avatar": user.avatar,
                },
            )
        return history
