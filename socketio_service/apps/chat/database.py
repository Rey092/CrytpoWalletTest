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
        await user.create()

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
        user = await self.chat_user.get(user_id)
        update_query = {"$set": {"online": online}}
        await user.update(update_query)
