# -*- coding: utf-8 -*-
from fastapi import APIRouter, Request
from pydantic import BaseModel
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

profile_front_router = APIRouter()

templates = Jinja2Templates(directory="templates")


@profile_front_router.get("/get", response_class=HTMLResponse)
async def get(request: Request):
    if request.cookies.get("Authorization"):
        return templates.TemplateResponse("profile/get_profile.html", {"request": request})
    return RedirectResponse("/front/auth/login")


class User(BaseModel):
    email: str
    password: str
