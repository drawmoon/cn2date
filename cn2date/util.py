# pyright: strict

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

import tomli
from dateutil.relativedelta import relativedelta
from pkg_resources import resource_stream
from typing_extensions import Literal


def get_settings() -> dict[str, Any]:
    """
    获取应用配置，读取 `settings.toml` 配置文件
    :return:
    """

    with resource_stream("cn2date", "settings.toml") as stream:
        return tomli.load(stream)  # type: ignore


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
    fmt: Literal["y", "fhoy", "shoy", "q", "fq", "sq", "tq", "foq", "m", "w", "d", "am", "pm"],
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
    fmt: Literal["y", "fhoy", "shoy", "q", "fq", "sq", "tq", "foq", "m", "w", "d", "am", "pm"],
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

    :rtype: object
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

    示例:

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
    part = st.cn2numstr(text)

    if not part.isdigit():
        raise TypeError("Conversion failed")

    if typ == "y" and len(part) == 2:
        part = str(now().year)[0:2] + part

    return int(part)


class SimpleTransform:
    """ """

    chart = {"0": "零", "1": "一", "2": "二", "3": "三", "4": "四", "5": "五", "6": "六", "7": "七", "8": "八", "9": "九"}

    num2cn_tb = str.maketrans(chart)
    cn2num_tb = str.maketrans(dict(zip(list(chart.values()), list(chart.keys()))))

    def num2cn(self, text: str, strict: bool = False) -> str:
        """

        :param text:
        :param strict: 严格模式，当值为 True 时，严格按照中文标准翻译，例如："10" -> "十"
            值为 False 时则按 chart 简单映射翻译，例如："10" -> "一零"，默认为 False
        :return:
        """
        val = text.translate(self.num2cn_tb)
        if not strict:
            return val

        str_list: list[str] = []
        if len(val) == 2:
            # 处理 "十x" 的字符串
            if val[0] != "零":
                if val[1] == "零":
                    str_list.append(val[0])
                    str_list.append("十")
                else:
                    str_list.append(val[0])
                    str_list.append("十")
                    str_list.append(val[1])
                return "".join(str_list[1:]) if str_list[0] == "一" else "".join(str_list)

        return val

    def cn2numstr(self, text: str) -> str:
        """
        将汉字数字转换为阿拉伯数字

        例如：
            `"一二三四五六"` -> `"123456"` \n
            `"零一"` -> `"01"` \n
            `"十一"` -> `"11"` \n
        :param text:
        :return:
        """
        d = {"十": "10", "两": "2"}
        if text in d:
            return d[text]

        val = text.translate(self.cn2num_tb)

        if val[0] == "十":
            return f"1{val[1:]}"

        # 处理 "x十" 的字符串
        if len(val) >= 2 and val[1] == "十":
            str_list: list[str] = []
            if len(val) == 2:
                str_list.append(val[:-1])
                str_list.append("0")
            else:
                str_list.append(val[0])
                str_list.append(val[2])
            return "".join(str_list)

        return val


def isblank(s: str | None) -> bool:
    """
    检查字符串是否为空格、空 ("") 或 None。
    :param s:
    :return: 如果为空格、空 ("") 或 None 则返回 True，否则返回 False
    """
    return s is None or not s or s.isspace()
