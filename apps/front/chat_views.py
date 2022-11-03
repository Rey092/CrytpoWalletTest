# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from apps.front.dependencies import check_user_token

chat_front_router = APIRouter()

templates = Jinja2Templates(directory="templates")


@chat_front_router.get("/messages", response_class=HTMLResponse, include_in_schema=False)
async def login(
    request: Request,
    token=Depends(check_user_token),
):
    if token is None:
        return RedirectResponse("/auth/login")
    return templates.TemplateResponse("chat/list_messages.html", {"request": request})
