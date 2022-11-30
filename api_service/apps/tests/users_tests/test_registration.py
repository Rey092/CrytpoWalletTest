# -*- coding: utf-8 -*-
import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from api_service.apps.users.schemas import UserRegister, UserRegisterResponse


@pytest.mark.anyio
async def test_registration_201(client: AsyncClient, fastapi_app: FastAPI):
    data = UserRegister(
        email="test1@gmail.com",
        username="Test User",
        password1="Zaqwerty123#",
        password2="Zaqwerty123#",
    )
    url = fastapi_app.url_path_for("register")
    response = await client.post(
        url,
        json=data.dict(),
    )
    assert response.status_code == 201
    assert UserRegisterResponse(**response.json())


@pytest.mark.anyio
async def test_registration_400(client: AsyncClient, fastapi_app: FastAPI):
    data = UserRegister(
        email="test4@example.com",
        username="Test ### User",
        password1="Zaqwerty123#",
        password2="Zaqwerty123#",
    )
    url = fastapi_app.url_path_for("register")
    response = await client.post(
        url,
        json=data.dict(),
    )
    assert response.status_code == 400


@pytest.mark.anyio
async def test_registration_422(client: AsyncClient, fastapi_app: FastAPI):
    url = fastapi_app.url_path_for("register")
    response = await client.post(
        url,
        json={},
    )
    assert response.status_code == 422
