# -*- coding: utf-8 -*-
import pytest
from fastapi import FastAPI
from httpx import AsyncClient


@pytest.mark.anyio
async def test_get_profile(
    client: AsyncClient,
    fastapi_app: FastAPI,
    user_token,
):
    url = fastapi_app.url_path_for("get")
    response = await client.get(
        url,
    )
    assert response.status_code == 200
