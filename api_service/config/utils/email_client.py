# -*- coding: utf-8 -*-
from functools import lru_cache
from pathlib import Path

from fastapi_helper.schemas.camel_schema import ApiSchema
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr

from api_service.config.settings import settings


class EmailSchema(ApiSchema):
    email: EmailStr
    username: str


class EmailClient:
    """
    EmailClient, Native Email Client using aiosmtplib, help to send
    emails, and confirm emails, also if the user forgot his password.
    """

    def __init__(
        self,
        username: str,
        host: str,
        port: int,
        password: str,
        use_tls: bool,
        use_ssl: bool,
        mail_from: str,
        display_name: str,
    ):
        self._conf = ConnectionConfig(
            MAIL_SERVER=host,
            MAIL_PORT=port,
            MAIL_USERNAME=username,
            MAIL_PASSWORD=password,
            MAIL_FROM=mail_from,
            MAIL_STARTTLS=use_tls,
            MAIL_SSL_TLS=use_ssl,
            TEMPLATE_FOLDER=Path(__file__).parent.parent.parent.parent / "templates/emails",
        )
        self._connection = FastMail(self._conf)
        self.mail_from = mail_from
        self.display_name = display_name

    async def send_email_to_new_user(self, data: EmailSchema) -> None:
        message = MessageSchema(
            subject="Fastapi-Mail module",
            recipients=[data.email],
            template_body={"username": data.username},
            subtype=MessageType.html,
        )
        await self._connection.send_message(message, template_name="new_user.html")


@lru_cache()
def create_email_client() -> EmailClient:
    return EmailClient(
        username=settings.smtp_user,
        host=settings.smtp_host,
        port=settings.smtp_port,
        password=settings.smtp_pass,
        use_tls=settings.smtp_use_tls,
        use_ssl=settings.smtp_use_ssl,
        mail_from=settings.smtp_mail_from,
        display_name=settings.site_name,
    )
