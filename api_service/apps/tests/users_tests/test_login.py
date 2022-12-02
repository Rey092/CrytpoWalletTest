# -*- coding: utf-8 -*-
import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from api_service.apps.users.schemas import UserLogin, UserLoginResponse


@pytest.mark.anyio
async def test_login_200(client: AsyncClient, fastapi_app: FastAPI, get_user_data: UserLogin):
    url = fastapi_app.url_path_for("login")
    response = await client.post(
        url,
        json=get_user_data.dict(),
    )
    assert response.status_code == 200
    assert UserLoginResponse(**response.json())


@pytest.mark.anyio
async def test_login_401(client: AsyncClient, fastapi_app: FastAPI, get_user_data: UserLogin):
    url = fastapi_app.url_path_for("login")
    get_user_data.password = "12345"
    response = await client.post(
        url,
        json=get_user_data.dict(),
    )
    assert response.status_code == 401


@pytest.mark.anyio
async def test_login_422(client: AsyncClient, fastapi_app: FastAPI):
    url = fastapi_app.url_path_for("login")
    response = await client.post(
        url,
        json={},
    )
    assert response.status_code == 422
