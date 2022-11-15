# -*- coding: utf-8 -*-
import motor.motor_asyncio

from socketio_service.apps.chat.models import ChatMessage, ChatUser
from socketio_service.config.settings import settings

client = motor.motor_asyncio.AsyncIOMotorClient(str(settings.mongodb_url))
db = client[settings.mongodb_name]
collections = [ChatMessage, ChatUser]
