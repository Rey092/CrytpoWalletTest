# -*- coding: utf-8 -*-
from sqladmin import ModelView

from api_service.apps.crypto.models import Asset, Transaction, Wallet
from api_service.apps.product.models import Order, Product
from api_service.apps.users.models import Permission, User


class UserAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.username,
        User.email,
        User.avatar,
        User.is_active,
        User.count_messages,
    ]
    column_searchable_list = [User.id, User.email, User.username]
    icon = "fa-solid fa-user"


class PermissionAdmin(ModelView, model=Permission):
    column_list = [
        Permission.id,
        Permission.user_id,
        Permission.has_access_chat,
    ]
    column_searchable_list = [Permission.id, Permission.user_id]
    icon = "fa-solid fa-key"


class WalletAdmin(ModelView, model=Wallet):
    column_list = [
        Wallet.id,
        Wallet.address,
        Wallet.balance,
        Wallet.user_id,
        Wallet.asset_id,
        Wallet.date_created,
        Wallet.private_key,
    ]
    column_sortable_list = [Wallet.date_created]
    column_searchable_list = [Wallet.id, Wallet.address, Wallet.user_id]
    icon = "fa-solid fa-wallet"


class TransactionAdmin(ModelView, model=Transaction):
    column_list = [
        Transaction.txn_hash,
        Transaction.address_from,
        Transaction.address_to,
        Transaction.value,
        Transaction.txn_fee,
        Transaction.age,
        Transaction.status,
    ]
    column_sortable_list = [Transaction.age]
    column_searchable_list = [Transaction.txn_hash, Transaction.address_from, Transaction.address_to]
    icon = "fa-solid fa-file"


class AssetAdmin(ModelView, model=Asset):
    column_exclude_list = [
        Asset.wallets,
        Asset.transactions,
    ]
    icon = "fa-solid fa-gear"


class ProductAdmin(ModelView, model=Product):
    column_list = [
        Product.id,
        Product.title,
        Product.image,
        Product.price,
        Product.is_sold,
        Product.date_created,
        Product.wallet_id,
    ]
    column_sortable_list = [Product.date_created]
    column_searchable_list = [Product.id, Product.title, Product.wallet_id]
    icon = "fa-solid fa-gift"


class OrderAdmin(ModelView, model=Order):
    column_list = [
        Order.id,
        Order.status,
        Order.date,
        Order.buyer_address,
        Order.txn_hash,
        Order.txn_hash_return,
        Order.product_id,
    ]
    column_sortable_list = [Order.date]
    column_searchable_list = [Order.id, Order.product_id]
    icon = "fa-solid fa-truck-fast"
