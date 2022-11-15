# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional
from uuid import UUID

from beanie import Document
from pydantic import BaseModel


class ChatUser(Document):
    id: UUID
    username: str
    avatar: Optional[str] = None
    online: Optional[bool]

    class Settings:
        name = "chat_user"


class ChatMessage(Document):
    user_id: UUID
    message: str
    image: Optional[str] = None
    date: Optional[datetime]

    class Settings:
        name = "chat_message"


class UserModel(BaseModel):
    id: UUID
    avatar: Optional[str] = None
    username: str
    online: bool
