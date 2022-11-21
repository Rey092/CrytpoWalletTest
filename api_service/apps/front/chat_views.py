# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Request
from fastapi_contrib.permissions import PermissionsDependency
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from api_service.apps.front.dependencies import check_permission, check_user_token
from api_service.apps.front.permissions import ChatPermission

chat_front_router = APIRouter()

templates = Jinja2Templates(directory="templates")


@chat_front_router.get(
    "/messages",
    response_class=HTMLResponse,
    include_in_schema=False,
    dependencies=[
        Depends(PermissionsDependency([ChatPermission])),
    ],
)
async def get_chat(
    request: Request,
    token=Depends(check_user_token),
    user=Depends(check_permission),
):
    if token is None:
        return RedirectResponse("/auth/login")
    # if user is None or user.permission.has_access_chat is False:
    #     return RedirectResponse("/profile/get")
    return templates.TemplateResponse("chat/list_messages.html", {"request": request})
