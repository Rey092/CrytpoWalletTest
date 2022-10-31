# -*- coding: utf-8 -*-
from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

auth_front_router = APIRouter()

templates = Jinja2Templates(directory="templates")


@auth_front_router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    if request.cookies.get("Authorization"):
        return RedirectResponse("/profile/get")
    return templates.TemplateResponse("users/login.html", {"request": request})


@auth_front_router.get("/registration", response_class=HTMLResponse)
async def registration(request: Request):
    if request.cookies.get("Authorization"):
        return RedirectResponse("/profile/get")
    return templates.TemplateResponse("users/registration.html", {"request": request})
