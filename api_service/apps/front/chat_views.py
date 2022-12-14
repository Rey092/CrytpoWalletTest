# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from api_service.apps.front.dependencies import check_permission, check_user_token

chat_front_router = APIRouter()

templates = Jinja2Templates(directory="templates")


@chat_front_router.get(
    "/messages",
    response_class=HTMLResponse,
    include_in_schema=False,
)
async def get_chat(
    request: Request,
    token=Depends(check_user_token),
    user=Depends(check_permission),
):
    if token is None:
        return RedirectResponse("/auth/login")
    if user is None or user.permission.has_access_chat is False:
        return RedirectResponse("/profile/get")
    return templates.TemplateResponse("chat/list_messages.html", {"request": request})


@chat_front_router.get("/asyncapi_docs", response_class=HTMLResponse, include_in_schema=False)
async def asyncapi_docs(
    request: Request,
):
    return templates.TemplateResponse("chat/asyncapi/index.html", {"request": request})
