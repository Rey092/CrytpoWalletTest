# -*- coding: utf-8 -*-
import enum


class OrderStatus(enum.Enum):
    NEW = "NEW"
    DELIVERY = "DELIVERY"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"
    RETURN = "RETURN"
