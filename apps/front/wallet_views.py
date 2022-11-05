# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from apps.front.dependencies import check_user_token

wallets_front_router = APIRouter()


templates = Jinja2Templates(directory="templates")


@wallets_front_router.get(
    "/",
    response_class=HTMLResponse,
    include_in_schema=False,
)
async def get(
    request: Request,
    token=Depends(check_user_token),
):
    if token is None:
        return RedirectResponse("/auth/login")
    return templates.TemplateResponse("wallets/wallets_page.html", {"request": request})
