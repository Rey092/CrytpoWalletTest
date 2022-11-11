# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional
from uuid import UUID

from beanie import Document


class ChatUser(Document):
    id: UUID
    username: str
    avatar: str

    class Settings:
        name = "chat_user"


class ChatMessage(Document):
    user_id: UUID
    message: str
    image: Optional[str] = None
    date: Optional[datetime]

    class Settings:
        name = "chat_message"

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "message": "Test message",
    #             "image": "Test image",
    #             "date": datetime.now()
    #         }
    #     }
