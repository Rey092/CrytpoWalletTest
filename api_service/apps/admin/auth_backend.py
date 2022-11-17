# -*- coding: utf-8 -*-
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request


class MyBackend(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        if username == "admin" and password == "Zaqwerty123":
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
