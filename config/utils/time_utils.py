# -*- coding: utf-8 -*-
from datetime import date, datetime
from typing import Tuple, Union

import pendulum
from pendulum import DateTime
from pytz import UTC

from apps.crypto.enums import FilterPeriod


def date_start_of_day(date: datetime.date) -> datetime:
    return datetime.combine(date, datetime.min.time(), tzinfo=UTC)


def date_end_of_day(date: datetime.date) -> datetime:
    return datetime.combine(date, datetime.max.time(), tzinfo=UTC)


def get_period(period: FilterPeriod) -> Union[Tuple[date, date], None]:
    today = pendulum.now(tz="UTC")
    if period == FilterPeriod.last_week.value:
        return (
            today.start_of("week").date(),
            today.end_of("week").date(),
        )
    if period == FilterPeriod.previous_week.value:
        return (
            today.subtract(days=7).start_of("week").date(),
            today.subtract(days=7).end_of("week").date(),
        )
    if period == FilterPeriod.last_month.value:
        return (
            today.start_of("month").date(),
            today.end_of("month").date(),
        )
    if period == FilterPeriod.previous_month.value:
        return (
            today.subtract(months=1).start_of("month").date(),
            today.subtract(months=1).end_of("month").date(),
        )
    if period == FilterPeriod.last_year.value:
        return (
            today.start_of("year").date(),
            today.end_of("year").date(),
        )
    if period == FilterPeriod.previous_year.value:
        return (
            today.subtract(years=1).start_of("year").date(),
            today.subtract(years=1).end_of("year").date(),
        )
    return None


def get_days_between_dates(start_date: DateTime, end_date: DateTime) -> int:
    date_diff = end_date - start_date
    return date_diff.in_days()
