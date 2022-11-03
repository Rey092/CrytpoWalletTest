# -*- coding: utf-8 -*-


def format_date(obj):
    obj.age = obj.age.strftime("%d.%m.%Y %H:%M")
    return obj
