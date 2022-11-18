# -*- coding: utf-8 -*-
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from api_service.config.settings import settings


class MyBackend(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        if username == settings.superuser_username and password == settings.superuser_password:
            request.session.update({"token": "..."})
            return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False
        return True
