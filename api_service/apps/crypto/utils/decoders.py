# -*- coding: utf-8 -*-
from datetime import datetime, timedelta


class BaseDecoder:
    @staticmethod
    def timestamp_to_period(time_stamp):
        date_time = datetime.fromtimestamp(int(time_stamp)) if time_stamp else datetime.now()
        return date_time

    @staticmethod
    def str_to_date(str_date):
        str_date = str_date.replace("T", " ").replace(".000Z", "")
        date_time = datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S") + timedelta(hours=2)
        return date_time
