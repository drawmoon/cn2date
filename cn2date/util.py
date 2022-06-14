from datetime import datetime
from typing import Literal, Optional

from dateutil.relativedelta import relativedelta


def now() -> datetime:
    return datetime.now()


class DateBuilder:
    def __init__(self):
        self.__date = datetime(now().year, 1, 1)

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
    fmt: Literal[
        "y", "fhoy", "shoy", "q", "fq", "sq", "tq", "foq", "m", "w", "d", "am", "pm"
    ],
) -> datetime:
    """
    参数::

        dt:

        fmt:
            - y: 年
            - fhoy: 上半年
            - shoy: 下半年
            - q: 季度
            - fq: 第一季度
            - sq: 第二季度
            - tq: 第三季度
            - foq: 第四季度
            - m: 月
            - w: 周
            - d: 天
            - am: 上午
            - pm: 下午

    :返回值:

    返回一个 :class:`datetime.datetime` 对象。

    """

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
    fmt: Literal[
        "y", "fhoy", "shoy", "q", "fq", "sq", "tq", "foq", "m", "w", "d", "am", "pm"
    ],
) -> datetime:
    """

    参数::

        dt:

        fmt:
            - y: 年
            - fhoy: 上半年
            - shoy: 下半年
            - q: 季度
            - fq: 第一季度
            - sq: 第二季度
            - tq: 第三季度
            - foq: 第四季度
            - m: 月
            - w: 周
            - d: 天
            - am: 上午
            - pm: 下午

    :返回值:

    返回一个 :class:`datetime.datetime` 对象。

    """

    if dt is None:
        raise ValueError("The parameter dt is None")

    if fmt == "y":
        return date_add(dt, 1, fmt)

    if fmt == "fhoy":
        return datetime(dt.year, 7, 1)

    if fmt == "shoy":
        return date_add(datetime(dt.year, 1, 1), 1, "y")

    if fmt == "q":
        return date_add(dt, 1, fmt)

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
    """
    `date_add()` 函数将一个时间/日期区间添加到一个日期中，然后返回该日期。

    参数::

        dt:
            要修改的日期。

        val:
            要添加的时间/日期间隔的值。

        fmt:
            要添加的区间的类型。可以是以下值之一:

            - y: 年
            - q: 季度
            - m: 月
            - w: 周
            - d: 天

    示例

    >>> from cn2date.util import date_sub
    >>> dt = datetime(2020, 1, 1)
    >>> date_add(dt, 1, "y")
    datetime.datetime(2021, 1, 1)

    :返回值:

    返回一个 :class:`datetime.datetime` 对象。

    """

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
    """
    `date_sub()` 函数从一个日期中减去一个时间/日期区间，然后返回日期。

    参数::

        dt:
            要修改的日期。

        val:
            要减去的时间/日期区间的值。

        fmt:
            要减去的区间的类型。可以是以下值之一:

            - y: 年
            - q: 季度
            - m: 月
            - w: 周
            - d: 天

    示例

    >>> from cn2date.util import date_sub
    >>> dt = datetime(2020, 1, 1)
    >>> date_sub(dt, 1, "y")
    datetime.datetime(2019, 1, 1)

    :返回值:

    返回一个 :class:`datetime.datetime` 对象。

    """

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


def date_part(text: str, typ: Optional[Literal["y"]] = None) -> int:
    st = SimpleTransform()
    part = st.cn2num(text)

    if not part.isdigit():
        raise TypeError("Conversion failed")

    if typ == "y" and len(part) == 2:
        part = str(now().year)[0:2] + part

    return int(part)


class SimpleTransform:
    _0 = "零"
    _1 = "一"
    _10 = "十"
    d = {
        "0": _0,
        "1": _1,
        "2": "二",
        "3": "三",
        "4": "四",
        "5": "五",
        "6": "六",
        "7": "七",
        "8": "八",
        "9": "九",
    }

    num2cn_tb = str.maketrans(d)
    cn2num_tb = str.maketrans(dict(zip(list(d.values()), list(d.keys()))))

    def num2cn(self, s: str, cast_chart_ten=False) -> str:
        val = s.translate(self.num2cn_tb)

        if cast_chart_ten and len(val) == 2 and val[0] != self._0:
            val = (
                f"{val[0]}{self._10}"
                if val[1] == self._0
                else f"{val[0]}{self._10}{val[1]}"
            )
            return val[1:] if val[0] == self._1 else val

        return val

    def cn2num(self, s: str):
        if s == self._10:
            return "10"

        val = s.translate(self.cn2num_tb)

        if val[0] == self._10:
            return f"1{val[1:]}"

        if len(val) >= 2 and val[1] == self._10:
            return f"{val[:-1]}0" if len(val) == 2 else f"{val[0]}{val[2]}"

        return val
