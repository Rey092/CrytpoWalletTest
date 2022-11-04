# -*- coding: utf-8 -*-
from datetime import datetime


def timestamp_to_period(start, end):
    date_start = datetime.fromtimestamp(int(start))
    date_end = datetime.fromtimestamp(int(end))
    period = date_end - date_start
    return int(period.total_seconds())
