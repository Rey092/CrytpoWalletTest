# -*- coding: utf-8 -*-
import datetime
from typing import Optional
from uuid import UUID

from asyncapi_schema_pydantic import (
    AmqpChannelBinding,
    AmqpQueue,
    AsyncAPI,
    ChannelBindings,
    ChannelItem,
    Components,
    Info,
    Message,
    Operation,
    Tag,
    WebSocketsChannelBinding,
)
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    avatar: Optional[str] = None


class Session(User):
    sid: str


class ChatMessage(BaseModel):
    message: str
    image: Optional[str] = None
    date: Optional[datetime.datetime]
    user_id: UUID
    username: str
    avatar: Optional[str] = None


# Construct AsyncAPI by pydantic objects
async_api = AsyncAPI(
    info=Info(
        title="Socket.IO chat service",
        version="1.0.0",
        description="Some description",
    ),
    servers={
        "socketio": {
            "url": "http://127.0.0.1:8002/ws/socket.io",
            "protocol": "wss",
            "protocolVersion": "5",
            "description": "Socketio development server",
        },
        "rabbitmq": {
            "url": "amqp://localhost:5672",
            "protocol": "amqp",
            "protocolVersion": "0.9.1",
            "description": "RabbitMQ development server",
        },
    },
    channels={
        "connect": ChannelItem(
            description="This channel is used for connecting users",
            bindings=ChannelBindings(
                ws=WebSocketsChannelBinding(),
            ),
            publish=Operation(
                summary="User connected.",
                message={
                    "$ref": "#/components/messages/UserData",
                },
            ),
            subscribe=Operation(
                summary="Server got new connection.",
                message={
                    "$ref": "#/components/messages/UserData",
                },
            ),
        ),
        "success_connect": ChannelItem(
            description="This channel is used for create session for users. Adding users to chat room",
            bindings=ChannelBindings(
                ws=WebSocketsChannelBinding(),
            ),
            publish=Operation(
                summary="Server emit data and sid for new user.",
                message={
                    "$ref": "#/components/messages/SessionData",
                },
            ),
            subscribe=Operation(
                summary="Get user session.",
                message={
                    "$ref": "#/components/messages/SessionData",
                },
            ),
        ),
        "get_online_users": ChannelItem(
            description="This channel is used for check online user",
            bindings=ChannelBindings(
                ws=WebSocketsChannelBinding(),
            ),
            publish=Operation(
                summary="Server emit all online users.",
                message={
                    "$ref": "#/components/messages/OnlineUsers",
                },
            ),
            subscribe=Operation(
                summary="Get online users.",
                message={
                    "$ref": "#/components/messages/OnlineUsers",
                },
            ),
        ),
        "get_history": ChannelItem(
            description="This channel is used for get chat history",
            bindings=ChannelBindings(
                ws=WebSocketsChannelBinding(),
            ),
            publish=Operation(
                summary="Server emit chat history.",
                message={
                    "$ref": "#/components/messages/ChatHistory",
                },
            ),
            subscribe=Operation(
                summary="Get chat history.",
                message={
                    "$ref": "#/components/messages/ChatHistory",
                },
            ),
        ),
        "new_message": ChannelItem(
            description="This channel is used for exchange of new messages between users",
            bindings=ChannelBindings(
                ws=WebSocketsChannelBinding(),
            ),
            publish=Operation(
                summary="User send new message.",
                message={
                    "$ref": "#/components/messages/NewMessage",
                },
            ),
            subscribe=Operation(
                summary="User get new messages.",
                message={
                    "$ref": "#/components/messages/NewMessage",
                },
            ),
        ),
        "user_detail": ChannelItem(
            description="This channel is used for get additional info about online user",
            bindings=ChannelBindings(
                ws=WebSocketsChannelBinding(),
            ),
            publish=Operation(
                summary="Server emit additional info about user.",
                message={
                    "$ref": "#/components/messages/UserInfo",
                },
            ),
            subscribe=Operation(
                summary="User get additional info about another user.",
                message={
                    "$ref": "#/components/messages/UserInfo",
                },
            ),
        ),
        "disconnect": ChannelItem(
            description="This channel is used for disconnecting users",
            bindings=ChannelBindings(
                ws=WebSocketsChannelBinding(),
            ),
            publish=Operation(
                summary="User disconnect from chat.",
                message={
                    "$ref": "#/components/messages/SessionData",
                },
            ),
            subscribe=Operation(
                summary="Server get session for deleting.",
                message={
                    "$ref": "#/components/messages/SessionData",
                },
            ),
        ),
        "count_messages_exchange": ChannelItem(
            description="This channel counts the number of messages after the current user disconnects",
            bindings=ChannelBindings(
                amqp=AmqpChannelBinding(
                    param_is="queue",
                    queue=AmqpQueue(
                        name="message-queue",
                        durable=True,
                        exclusive=True,
                        autoDelete=False,
                        vhost="/",
                    ),
                ),
            ),
            publish=Operation(
                summary="Publish updated count of messages for user.",
                message={
                    "$ref": "#/components/messages/NewMessage",
                },
            ),
        ),
    },
    components=Components(
        messages={
            "UserData": Message(
                name="User",
                title="User Data",
                summary="Action to connect to server.",
                description="Get user data after success connection",
                contentType="application/json",
                tags=[
                    Tag(name="User connect"),
                    Tag(name="User data"),
                ],
                payload={
                    "$ref": "#/components/schemas/User",
                },
            ),
            "SessionData": Message(
                name="Session",
                title="Session Data",
                summary="Action to got session.",
                description="Get user session after success connection",
                contentType="application/json",
                tags=[
                    Tag(name="User session"),
                ],
                payload={
                    "$ref": "#/components/schemas/Session",
                },
            ),
            "OnlineUsers": Message(
                name="OnlineUsers",
                title="Online Users",
                summary="Action to got online users.",
                description="Get online users after success connection",
                contentType="application/json",
                tags=[
                    Tag(name="Online Users"),
                ],
                payload={
                    "$ref": "#/components/schemas/User",
                },
            ),
            "ChatHistory": Message(
                name="ChatHistory",
                title="Chat History",
                summary="Action to got chat history.",
                description="Get chat history after success connection",
                contentType="application/json",
                tags=[
                    Tag(name="Chat History"),
                ],
                payload={
                    "$ref": "#/components/schemas/ChatMessage",
                },
            ),
            "NewMessage": Message(
                name="NewMessage",
                title="New Message",
                summary="Action to got new messages.",
                description="Get new messages in chat",
                contentType="application/json",
                tags=[
                    Tag(name="New Message"),
                ],
                payload={
                    "$ref": "#/components/schemas/ChatMessage",
                },
            ),
            "UserInfo": Message(
                name="UserInfo",
                title="User Info",
                summary="Action to got user info.",
                description="Get additional info about another user",
                contentType="application/json",
                tags=[
                    Tag(name="User"),
                    Tag(name="Additional Info"),
                ],
                payload={
                    "$ref": "#/components/schemas/User",
                },
            ),
        },
        schemas={
            "User": User.schema(),
            "Session": Session.schema(),
            "ChatMessage": ChatMessage.schema(),
        },
    ),
)

json_data = async_api.json(by_alias=True, exclude_none=True, indent=2)

# recursively delete "oneOf", "anyOf", "allOf", "enum" keys if they are []
for_delete = ['"oneOf": [],\n', '"anyOf": [],\n', '"allOf": [],\n', '"enum": [],\n']
for key in for_delete:
    json_data = json_data.replace(key, "")

# dump to file sample.yaml
with open("docs.yaml", "w") as f:
    f.write(json_data)
