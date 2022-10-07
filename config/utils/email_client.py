# -*- coding: utf-8 -*-
from functools import lru_cache
from pathlib import Path
from typing import List

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from pydantic import BaseModel, EmailStr

from config.settings import settings


class EmailSchema(BaseModel):
    email: List[EmailStr]


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
        frontend_url: str,
        backend_url: str,
    ):
        self._conf = ConnectionConfig(
            MAIL_SERVER=host,
            MAIL_PORT=port,
            MAIL_USERNAME=username,
            MAIL_PASSWORD=password,
            MAIL_FROM=mail_from,
            MAIL_TLS=use_tls,
            MAIL_SSL=use_ssl,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True,
            TEMPLATE_FOLDER=Path(__file__).parent.parent.parent / "templates/emails",
        )
        self._connection = FastMail(self._conf)
        self.mail_from = mail_from
        self.display_name = display_name
        self.frontend_url = frontend_url
        self.backend_url = backend_url

    async def send_confirmation_email(self, email: EmailSchema, secret_string: str) -> None:
        message = MessageSchema(
            subject="Confirm email",
            recipients=email.dict().get("email"),
            # text=f"""Welcome to <a href="{self.frontend_url}">{self.frontend_url}</a>!<br /><br />
            # <a href="{self.frontend_url}/confirm?token={secret_string}">Click here</a> to
            # complete your sing up<br /><br />Thanks,<br />{self.frontend_url} team""",
            template_body={"frontend_url": self.frontend_url, "token": secret_string},
            subtype="html",
        )
        await self._connection.send_message(message, template_name="confirm_email.html")

    async def send_forgot_password_email(self, email: EmailSchema, secret_string: str) -> None:
        message = MessageSchema(
            subject="Forgot password",
            recipients=email.dict().get("email"),
            # html=f"""Password reset has been requested for <a href="{self.frontend_url}">{self.frontend_url}</a><br />
            # <br />If it was you who did it, <a href="{self.frontend_url}/reset_password?token={secret_string}">
            # click here</a><br /><br /><br /><br />If it was not you, ignore this letter.<br /><br />
            # Thanks,<br />{self.frontend_url} team""",
            template_body={"frontend_url": self.frontend_url, "token": secret_string},
            subtype="html",
        )
        await self._connection.send_message(message, template_name="forgot_password.html")

    async def send_message(self, message: MessageSchema) -> None:
        await self._connection.send_message(message)


@lru_cache()
def create_email_client() -> EmailClient:
    return EmailClient(
        username=settings.smtp_user,
        host=settings.smtp_host,
        port=settings.smtp_port,
        password=settings.smtp_pass,
        use_tls=settings.smtp_use_tls,
        use_ssl=settings.smtp_use_ssl,
        mail_from="test@gmail.com",
        display_name=settings.site_name,
        frontend_url=settings.frontend_url,
        backend_url=settings.backend_url,
    )
