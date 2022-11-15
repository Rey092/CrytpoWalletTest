# -*- coding: utf-8 -*-
from datetime import datetime


class BaseDecoder:
    @staticmethod
    def timestamp_to_period(time_stamp):
        date_time = datetime.fromtimestamp(int(time_stamp)) if time_stamp else datetime.now()
        return date_time
