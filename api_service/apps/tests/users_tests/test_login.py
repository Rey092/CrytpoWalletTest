# -*- coding: utf-8 -*-
import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from api_service.apps.users.schemas import UserLogin, UserLoginResponse
from api_service.config.settings import settings


@pytest.mark.anyio
async def test_login(client: AsyncClient, fastapi_app: FastAPI):
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

    # 200
    assert response.status_code == 200
    assert UserLoginResponse(**response.json())

    # 422
    response = await client.post(
        url,
        json={},
    )
    assert response.status_code == 422

    # 401
    data.email = "test3@gmail.com"
    response = await client.post(
        url,
        json=data.dict(),
    )
    assert response.status_code == 401
