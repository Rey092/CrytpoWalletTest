# -*- coding: utf-8 -*-


def format_date(obj):
    obj.date = obj.date.strftime("%d.%m.%Y %H:%M")
    return obj
