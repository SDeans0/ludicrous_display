import datetime as dt
from typing import Optional


def get_today():
    return dt.date.today()


def get_now():
    return dt.datetime.now()


def get_start_of_day(day: Optional[dt.date] = None):
    day = day or get_today()
    return dt.datetime.combine(day, dt.time.min)
