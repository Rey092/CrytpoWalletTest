# -*- coding: utf-8 -*-
from fastapi import FastAPI

from ibay_service.apps.order import models
from ibay_service.apps.order.order_handler import order_handler_thread
from ibay_service.config.db import engine
from ibay_service.ibay_service_consumer import ibay_consumer_thread


def init_ibay_database() -> None:
    models.Base.metadata.create_all(bind=engine)


def create_app() -> FastAPI:
    app_ = FastAPI()

    # init needed utils
    init_ibay_database()

    # start needed threads
    ibay_consumer_thread.start()
    order_handler_thread.start()

    return app_


app = create_app()
