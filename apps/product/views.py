# -*- coding: utf-8 -*-
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from apps.product.dependencies import examples_generate, get_db, get_product_manager
from apps.product.exceptions import (
    InvalidBalanceException,
    InvalidPriceException,
    InvalidProductException,
    InvalidWalletException,
)
from apps.product.manager import ProductManager
from apps.product.schemas import OrderCreate, OrderDetail, ProductCreate, ProductDetail
from apps.users.models import User
from apps.users.user import get_current_user, get_current_user_payload
from config.storage import StorageException, ValidateFormatException

product_router = APIRouter()


# region Product
@product_router.get(
    "/products",
    responses=examples_generate.get_error_responses(auth=True),
    response_model=List[ProductDetail],
)
async def get_products(
    user: User = Depends(get_current_user_payload),  # noqa
    db: Session = Depends(get_db),
    product_manager: ProductManager = Depends(get_product_manager),
):
    """
    Get all products\n
    Permission: Is authenticated.
    """
    return await product_manager.get_all_products(db=db)


@product_router.post(
    "/products/create",
    status_code=status.HTTP_201_CREATED,
    responses=examples_generate.get_error_responses(
        InvalidPriceException,
        InvalidWalletException,
        ValidateFormatException,
        StorageException,
        auth=True,
    ),
    response_model=ProductDetail,
)
async def create_product(
    product: ProductCreate = Depends(ProductCreate.as_form),
    user: User = Depends(get_current_user_payload),  # noqa
    db: Session = Depends(get_db),
    product_manager: ProductManager = Depends(get_product_manager),
):
    """
    Create new product\n
    Permission: Is authenticated.
    """
    return await product_manager.create_new_product(db=db, product_create=product)


# endregion Product


# region Order
@product_router.get(
    "/orders",
    responses=examples_generate.get_error_responses(auth=True),
    response_model=List[OrderDetail],
)
async def get_my_orders(
    user: User = Depends(get_current_user),  # noqa
    db: Session = Depends(get_db),
    product_manager: ProductManager = Depends(get_product_manager),
):
    """
    Get all user's orders\n
    Permission: Is authenticated.
    """
    return await product_manager.get_users_orders(db, user.wallets)


@product_router.post(
    "/orders/create",
    status_code=status.HTTP_201_CREATED,
    responses=examples_generate.get_error_responses(
        InvalidProductException,
        InvalidWalletException,
        InvalidBalanceException,
        auth=True,
    ),
    response_model=OrderDetail,
)
async def create_order(
    order: OrderCreate,
    user: User = Depends(get_current_user),  # noqa
    db: Session = Depends(get_db),
    product_manager: ProductManager = Depends(get_product_manager),
):
    """
    Create new order\n
    wallet_id: Selected wallet for payment\n
    product_id: Product to checkout\n\n
    Permission: Is authenticated.
    """
    return await product_manager.create_new_order(db, order, user)


# endregion Order
