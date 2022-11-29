# -*- coding: utf-8 -*-
import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from api_service.apps.users.schemas import UserLogin
from api_service.config.settings import settings


@pytest.mark.anyio
async def test_login(client: AsyncClient, fastapi_app: FastAPI, user_token):
    data = UserLogin(
        email=settings.user_email,
        password=settings.user_password,
        remember_me=True,
    )

    url = fastapi_app.url_path_for("login")
    response = await client.post(
        url,
        json=data.dict(),
    )
    assert response.status_code == 200
