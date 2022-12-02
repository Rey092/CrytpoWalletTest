# -*- coding: utf-8 -*-
from typing import Type
from uuid import UUID

from beanie import PydanticObjectId

from socketio_service.apps.chat.models import ChatMessage, ChatUser


class ChatDatabase:
    """
    Chat database adapter for ChatMessage and ChatUser.
    """

    def __init__(
        self,
        chat_user: Type[ChatUser],
        chat_message: Type[ChatMessage],
    ):
        self.chat_user = chat_user
        self.chat_message = chat_message

    @staticmethod
    async def create_message(
        message: ChatMessage,
    ):
        return await message.create()

    async def list_message(self):
        return await self.chat_message.find_all().sort(-self.chat_message.date).limit(10).to_list()  # noqa

    async def get_user(
        self,
        user_id: UUID,
    ):
        return await self.chat_user.find_one(self.chat_user.id == user_id)

    @staticmethod
    async def create_user(
        user: ChatUser,
    ):
        try:
            await user.create()
        except Exception as ex:
            print(ex)

    async def get_online_users(
        self,
    ):
        return await self.chat_user.find({"online": True}, {}).to_list()

    async def update_user_status(
        self,
        data: dict,
        online: bool,
    ):
        user_id: PydanticObjectId = data.get("auth").get("id")
        sid = data.get("sid")
        user = await self.chat_user.get(user_id)
        update_query = {"$set": {"online": online, "sid": sid}}
        await user.update(update_query)

    async def disconnect_all_users(self):
        update_query = {"$set": {"online": False}}
        await self.chat_user.update_all(update_query)

    async def update_user(
        self,
        user_data: dict,
    ):
        user_id: PydanticObjectId = user_data.get("id")
        user = await self.chat_user.get(user_id)
        update_query = {
            "$set": {
                "username": user_data.get("username"),
                "avatar": user_data.get("avatar"),
            },
        }
        await user.update(update_query)

    async def get_count_message(
        self,
        user_id: UUID,
    ):
        return await self.chat_message.find({"user_id": user_id}, {}).to_list()
