# -*- coding: utf-8 -*-
import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from api_service.apps.users.schemas import UserProfile


@pytest.mark.anyio
async def test_get_profile_not_authenticated(
    client: AsyncClient,
    fastapi_app: FastAPI,
):
    url = fastapi_app.url_path_for("get_profile")
    response = await client.get(
        url,
    )
    assert response.status_code == 403


@pytest.mark.anyio
async def test_get_profile_authenticated(
    client: AsyncClient,
    fastapi_app: FastAPI,
    user_token,
):
    url = fastapi_app.url_path_for("get_profile")
    response = await client.get(
        url,
    )
    assert response.status_code == 200
    assert UserProfile(**response.json())
