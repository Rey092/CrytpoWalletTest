# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from api_service.apps.front.dependencies import check_user_token

profile_front_router = APIRouter()


templates = Jinja2Templates(directory="templates")


@profile_front_router.get(
    "/get",
    response_class=HTMLResponse,
    include_in_schema=False,
)
async def get(
    request: Request,
    token=Depends(check_user_token),
):
    if token is None:
        return RedirectResponse("/auth/login")
    return templates.TemplateResponse("profile/get_profile.html", {"request": request})
