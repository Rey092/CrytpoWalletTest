# -*- coding: utf-8 -*-
import base64
import datetime
from uuid import UUID

from socketio_service.apps.chat.database import ChatDatabase
from socketio_service.apps.chat.models import ChatMessage, ChatUser
from socketio_service.apps.chat.storage import MongoStorage


class ChatManager:
    def __init__(
        self,
        database: ChatDatabase,
        storage: MongoStorage,
    ):
        self.database = database
        self.storage = storage

    async def new_message(self, message: ChatMessage) -> dict:
        message.date = datetime.datetime.now()
        if message.image is not None:
            path = await self.storage.upload(
                file=base64.b64decode(message.image),
                upload_to="chat",
                sizes=(300, 300),
                content_types=["png", "jpg", "jpeg"],
            )
            message.image = path
        data = await self.database.create_message(message)
        data_message = {
            "id": str(data.id),
            "user_id": str(data.user_id),
            "message": data.message,
            "date": data.date.strftime("%d.%m, %H:%M"),
            "image": data.image,
        }
        return data_message

    async def get_user(self, user_id: UUID):
        return await self.database.get_user(user_id)

    async def create_user(self, user: ChatUser):
        await self.database.create_user(user)

    async def update_user(self, user: dict):
        await self.database.update_user(user)

    async def connect_user(self, data: dict):
        await self.database.update_user_status(data, True)

    async def disconnect_user(self, data: dict):
        await self.database.update_user_status(data, False)

    async def disconnect_all_users(self):
        await self.database.disconnect_all_users()

    async def get_online_users(self) -> list:
        data = await self.database.get_online_users()
        return [
            {
                "id": str(user.id),
                "username": user.username,
                "avatar": user.avatar,
                "sid": user.sid,
            }
            for user in data
        ]

    async def get_history_chat(self) -> list:
        history = []
        list_messages = await self.database.list_message()
        for message in list_messages:
            user = await self.get_user(message.user_id)
            if user:
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

    async def get_count_messages(
        self,
        data: dict,
    ):
        user_id: UUID = UUID(data.get("auth").get("id"))
        messages = await self.database.get_count_message(user_id)
        return {"count": len(messages), "user_id": str(user_id)}
