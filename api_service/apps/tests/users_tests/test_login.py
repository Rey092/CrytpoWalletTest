# -*- coding: utf-8 -*-
import pytest

from api_service.apps.users.schemas import UserLogin, UserRegister
from api_service.config.settings import settings


@pytest.mark.anyio
async def test_register(client):
    data = UserRegister(
        email="test_user_test8@gmail.com",
        username="Test User",
        password1="Zaqwerty123#",
        password2="Zaqwerty123#",
    )
    response = await client.post(
        "/api/auth/register",
        json=data.dict(),
    )
    assert response.status_code == 201


@pytest.mark.anyio
async def test_login(client):
    data = UserLogin(
        email=settings.user_email,
        password=settings.user_password,
        remember_me=True,
    )
    response = await client.post(
        "/api/auth/login",
        json=data.dict(),
    )
    assert response.status_code == 200


# @pytest.mark.anyio
# async def test_get_profile(client, user_token):
#     response = await client.get(
#         "/api/profile/get"
#     )
#     assert response.status_code == 200
