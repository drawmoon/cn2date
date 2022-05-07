import os
from datetime import datetime
from typing import Literal, Optional

from dateutil.relativedelta import relativedelta


def now() -> datetime:
    # 方便进行单元测试
    return (
        datetime(2021, 9, 1)
        if os.getenv("PYTHON_ENVIRONMENT", "") == "Test"
        else datetime.now()
    )


class DateBuilder:
    def __init__(self):
        self.__date = now()

    def year(self, year: int):
        self.__date = self.__date.replace(year=year)

    def month(self, month: int):
        self.__date = self.__date.replace(month=month)

    def day(self, day: int):
        self.__date = self.__date.replace(day=day)

    def build(self):
        return self.__date


def startof(
    dt: datetime,
    fmt: Literal["y", "fhoy", "shoy", "q", "fq", "sq", "tq", "foq", "m", "w", "d", "am", "pm"],
) -> datetime:
    if dt is None:
        raise ValueError("The parameter dt is None")

    if fmt == "y":
        return datetime(dt.year, 1, 1)

    if fmt == "fhoy":
        return datetime(dt.year, 1, 1)

    if fmt == "shoy":
        return datetime(dt.year, 7, 1)

    if fmt == "q":
        return datetime(dt.year, dt.month // 3 * 3 - 2, 1)

    if fmt == "fq":
        return datetime(dt.year, 1, 1)

    if fmt == "sq":
        return datetime(dt.year, 4, 1)

    if fmt == "tq":
        return datetime(dt.year, 7, 1)

    if fmt == "foq":
        return datetime(dt.year, 10, 1)

    if fmt == "m":
        return datetime(dt.year, dt.month, 1)

    if fmt == "w":
        return date_sub(dt, dt.weekday(), "d")

    if fmt == "d":
        return datetime(dt.year, dt.month, dt.day)

    if fmt == "am":
        return datetime(dt.year, dt.month, dt.day, 0, 0, 0)

    if fmt == "pm":
        return datetime(dt.year, dt.month, dt.day, 12, 0, 0)

    raise ValueError("The parameter fmt is invalid")


def endof(
    dt: datetime,
    fmt: Literal["y", "fhoy", "shoy", "q", "fq", "sq", "tq", "foq", "m", "w", "d", "am", "pm"],
) -> datetime:
    if dt is None:
        raise ValueError("The parameter dt is None")

    if fmt == "y":
        return date_add(dt, 1, "y")

    if fmt == "fhoy":
        return datetime(dt.year, 7, 1)

    if fmt == "shoy":
        return date_add(datetime(dt.year, 1, 1), 1, "y")

    if fmt == "q":
        return date_add(dt, 1, "q")

    if fmt == "fq":
        return datetime(dt.year, 4, 1)

    if fmt == "sq":
        return datetime(dt.year, 7, 1)

    if fmt == "tq":
        return datetime(dt.year, 10, 1)

    if fmt == "foq":
        return date_add(datetime(dt.year, 1, 1), 1, "y")

    if fmt == "m":
        return date_add(dt, 1, "m")

    if fmt == "w":
        return date_add(dt, 1, "w")

    if fmt == "d":
        return date_add(dt, 1, "d")

    if fmt == "am":
        return datetime(dt.year, dt.month, dt.day, 12, 0, 0)

    if fmt == "pm":
        return datetime(dt.year, dt.month, dt.day, 19, 0, 0)

    raise ValueError("The parameter fmt is invalid")


def date_add(dt: datetime, val: int, fmt: Literal["y", "q", "m", "w", "d"]) -> datetime:
    if dt is None:
        raise ValueError("The parameter dt is None")

    if fmt == "y":
        return dt + relativedelta(years=val)

    if fmt == "q":
        return dt + relativedelta(months=val * 3)

    if fmt == "m":
        return dt + relativedelta(months=val)

    if fmt == "w":
        return dt + relativedelta(days=val * 7)

    if fmt == "d":
        return dt + relativedelta(days=val)

    raise ValueError("The parameter fmt is invalid")


def date_sub(dt: datetime, val: int, fmt: Literal["y", "q", "m", "w", "d"]) -> datetime:
    if dt is None:
        raise ValueError("The parameter dt is None")

    if fmt == "y":
        return dt - relativedelta(years=val)

    if fmt == "q":
        return dt - relativedelta(months=val * 3)

    if fmt == "m":
        return dt - relativedelta(months=val)

    if fmt == "w":
        return dt - relativedelta(days=val * 7)

    if fmt == "d":
        return dt - relativedelta(days=val)

    raise ValueError("The parameter fmt is invalid")


def to_datepart(text: str, typ: Optional[str] = None) -> int:
    datepart = simple_transform(text)

    if not datepart.isdigit():
        raise TypeError("Conversion failed")

    if typ == "year" and len(datepart) == 2:
        datepart = str(now().year)[0:2] + datepart

    return int(datepart)


def simple_transform(n: str, cast_chart_ten = False) -> str:
    _0 = "零"
    _1 = "一"
    _10 = "十"
    t = { "0": _0, "1": _1, "2": "二", "3": "三", "4": "四", "5": "五", "6": "六", "7": "七", "8": "八", "9": "九" }
    
    val = n.translate(str.maketrans(t))

    if cast_chart_ten and len(val) == 2 and val[0] != _0:
        val = f"{val[0]}{_10}" if val[1] == _0 else f"{val[0]}{_10}{val[1]}"
        return val[1:] if val[0] == _1 else val
    return val
