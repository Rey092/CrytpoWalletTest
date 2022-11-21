# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from fastapi import Request
from starlette.responses import RedirectResponse


class RequiresLoginException(Exception):
    pass


class BasePermission(ABC):
    @abstractmethod
    def has_required_permissions(self, request: Request) -> bool:
        ...

    def __call__(self, request: Request):
        if not self.has_required_permissions(request):
            return RedirectResponse("/profile/get")


class ChatPermission(BasePermission):
    def has_required_permissions(self, request: Request) -> bool:
        return request.headers.get("User-Agent") == "Teapot v1.0"
