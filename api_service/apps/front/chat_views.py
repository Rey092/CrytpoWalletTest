# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from api_service.apps.front.dependencies import check_permission

chat_front_router = APIRouter()

templates = Jinja2Templates(directory="templates")


@chat_front_router.get("/messages", response_class=HTMLResponse, include_in_schema=False)
async def get_chat(
    request: Request,
    user=Depends(check_permission),
):
    if user is None or user.permission.has_access_chat is False:
        return RedirectResponse("/auth/login")
    return templates.TemplateResponse("chat/list_messages.html", {"request": request})
