# -*- coding: utf-8 -*-
import motor.motor_asyncio

from apps.socketio_app.models import ChatMessage, ChatUser
from config.settings import settings

client = motor.motor_asyncio.AsyncIOMotorClient(str(settings.mongodb_url))
db = client[settings.mongodb_name]
collections = [ChatMessage, ChatUser]
