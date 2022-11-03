# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from apps.front.dependencies import check_user_token

auth_front_router = APIRouter()

templates = Jinja2Templates(directory="templates")


@auth_front_router.get("/login", response_class=HTMLResponse, include_in_schema=False)
async def login(
    request: Request,
    token=Depends(check_user_token),
):
    if token:
        return RedirectResponse("/profile/get")
    return templates.TemplateResponse("users/login.html", {"request": request})


@auth_front_router.get("/registration", response_class=HTMLResponse, include_in_schema=False)
async def registration(request: Request):
    if request.cookies.get("Authorization"):
        return RedirectResponse("/profile/get")
    return templates.TemplateResponse("users/registration.html", {"request": request})
