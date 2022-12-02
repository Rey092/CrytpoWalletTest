# -*- coding: utf-8 -*-
from fastapi import FastAPI
from sqladmin import Admin
from sqlalchemy.engine import Engine

from api_service.apps.admin.auth_backend import MyBackend
from api_service.apps.admin.models import (
    AssetAdmin,
    OrderAdmin,
    PermissionAdmin,
    ProductAdmin,
    TransactionAdmin,
    UserAdmin,
    WalletAdmin,
)

authentication_backend = MyBackend(secret_key="...")


def init_sqladmin(app: FastAPI, engine: Engine):
    admin = Admin(
        app=app,
        engine=engine,
        authentication_backend=authentication_backend,
    )

    admin.add_view(UserAdmin)
    admin.add_view(PermissionAdmin)
    admin.add_view(WalletAdmin)
    admin.add_view(TransactionAdmin)
    admin.add_view(AssetAdmin)
    admin.add_view(ProductAdmin)
    admin.add_view(OrderAdmin)
