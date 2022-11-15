# -*- coding: utf-8 -*-
import datetime
from uuid import UUID

from socketio_service.apps.chat.database import ChatDatabase
from socketio_service.apps.chat.models import ChatMessage, ChatUser


class ChatManager:
    def __init__(
        self,
        database: ChatDatabase,
    ):
        self.database = database

    async def new_message(self, message: ChatMessage) -> None:
        message.date = datetime.datetime.now()
        await self.database.create_message(message)

    async def get_user(self, user_id: UUID):
        return await self.database.get_user(user_id)

    async def create_user(self, user: ChatUser):
        await self.database.create_user(user)

    async def connect_user(self, data: dict):
        await self.database.update_user_status(data, True)

    async def disconnect_user(self, data: dict):
        await self.database.update_user_status(data, False)

    async def get_online_users(self):
        data = await self.database.get_online_users()
        return [{"id": str(user.id), "username": user.username, "avatar": user.avatar} for user in data]

    async def get_history_chat(self):
        history = []
        list_messages = await self.database.list_message()
        for message in list_messages:
            user = await self.get_user(message.user_id)
            history.append(
                {
                    "message": message.message,
                    "image": message.image,
                    "date": message.date.strftime("%d.%m, %H:%M"),
                    "user_id": str(user.id),
                    "username": user.username,
                    "avatar": user.avatar,
                },
            )
        return history
