# -*- coding: utf-8 -*-
import inspect
from dataclasses import dataclass
from typing import Optional, Type

from fastapi import Form
from fastapi.exceptions import HTTPException
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param
from humps import camelize  # noqa
from pydantic import BaseModel
from pydantic.fields import ModelField
from starlette import status
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN
from tortoise.contrib.pydantic import PydanticModel

from config.settings import settings

metadata_tags = [
    {
        "name": "Health",
        "description": "Test health of the project.",
        "externalDocs": {
            "description": "Fastapi Docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
    {
        "name": "Auth",
        "description": "Roman // Authentication and authorization for crm users.",
    },
    {
        "name": "MobileAuth",
        "description": "Roman // Authentication and authorization for mobile users.",
    },
    {
        "name": "CRM Superuser",
        "description": "Roman // Superuser actions. Only for superusers.",
    },
    {
        "name": "CRM Staff Profile",
        "description": "Roman // Staff actions. For any staff.",
    },
    {
        "name": "CRM Users",
        "description": "Roman // Users data. For any staff.",
    },
    {
        "name": "Crypto",
        "description": "Roman // Base Crypto endpoints.",
    },
    {
        "name": "Ethereum",
        "description": f"Roman // ETH_API_URL={settings.eth_api_url.split('/')[0]},"
        f"ETHERSCAN_API_URL={settings.etherscan_api_url.split('/')[0]}",
    },
    {
        "name": "Tron",
        "description": f"Roman // TRON_GRID_API_URL={settings.tron_grid_api_url.split('/')[0]}",
    },
    {
        "name": "Bitcoin",
        "description": f"BLOCKCHAIN_INFO_API={settings.btc_api_url.split('/')[0]}",
    },
    {
        "name": "Litecoin",
        "description": f"BLOCKCYPHER_API={settings.blockcypher_ltc_api_url.split('/')[0]}",
    },
    {
        "name": "Binance Smart Chain",
        "description": f"BSCSCAN_API_URL={settings.bsc_scan_api_url.split('/')[0]} "
        f"BNB_API_URL={settings.bnb_api_url.split('/')[0]}",
    },
]


@dataclass
class ApiError:
    code: str
    type: str
    message: str
    exception: Type[Exception]
    status_code: Optional[int] = status.HTTP_400_BAD_REQUEST

    def example(self):
        example = {
            "summary": self.type,
            "value": {
                "detail": [
                    {
                        "code": self.code,
                        "type": self.type,
                        "message": self.message,
                    },
                ],
            },
        }
        return example

    def http_exception(self, message=None, headers=None):

        data = {
            "status_code": self.status_code,
            "detail": [
                {
                    "code": self.code,
                    "type": self.type,
                    "message": str(message) if message is not None and str(message) else self.message,
                },
            ],
        }
        return HTTPException(**data, headers=headers)

    def __hash__(self):
        return hash(self.code + self.type + self.message + str(self.status_code))


class JwtHTTPBearer(HTTPBearer):
    async def __call__(
        self,
        request: Request,
    ) -> Optional[HTTPAuthorizationCredentials]:
        authorization: str = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN,
                    detail={
                        "code": "bearer-001",
                        "type": "NOT_AUTHENTICATED",
                        "message": "Not authenticated",
                    },
                )
            else:
                return None
        if scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN,
                    detail={
                        "code": "bearer-001",
                        "type": "NOT_AUTHENTICATED",
                        "message": "Invalid authentication format",
                    },
                )
            else:
                return None
        return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)


jwt_http_bearer = JwtHTTPBearer()
jwt_http_bearer_no_error = JwtHTTPBearer(auto_error=False)


def as_form(cls: Type[BaseModel]):
    new_parameters = []

    for field_name, model_field in cls.__fields__.items():
        model_field: ModelField

        new_parameters.append(
            inspect.Parameter(
                model_field.alias,
                inspect.Parameter.POSITIONAL_ONLY,
                default=Form(...) if model_field.required else Form(model_field.default),
                annotation=model_field.outer_type_,
            ),
        )

    async def as_form_func(**data):
        return cls(**data)

    sig = inspect.signature(as_form_func)
    sig = sig.replace(parameters=new_parameters)
    as_form_func.__signature__ = sig  # type: ignore
    setattr(cls, "as_form", as_form_func)
    return cls


class ApiSchema(PydanticModel):
    class Config:
        orm_mode = True
        orig_model = None
        alias_generator = camelize
        allow_population_by_field_name = True
