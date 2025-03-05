import calendar
from datetime import datetime
from typing import List

from dateutil.relativedelta import relativedelta


class DateTime:
    def __init__(
        self, year=None, mon=None, day=None, hour=None, min=None, sec=None, millis=None
    ):
        self.year = 1970 if year is None else year
        self.mon = 1 if mon is None else mon
        self.day = 1 if day is None else day
        self.hour = 0 if hour is None else hour
        self.min = 0 if min is None else min
        self.sec = 0 if sec is None else sec
        self.millis = 0 if millis is None else millis

    @staticmethod
    def now():
        return DateTime.of(datetime.now())

    @staticmethod
    def of(d):
        if isinstance(d, DateTime):
            return DateTime(d.year, d.mon, d.day, d.hour, d.min, d.sec, d.millis)
        elif isinstance(d, datetime):
            return DateTime(
                d.year, d.month, d.day, d.hour, d.minute, d.second, d.microsecond
            )
        elif isinstance(d, str):
            return DateTime.of(datetime.strptime(d, "%Y-%m-%d %H:%M:%S"))
        elif isinstance(d, int):
            return DateTime.of(datetime.fromtimestamp(d / 1000))
        else:
            raise TypeError("Unsupported type: %s" % type(d))

    def last_year(self):
        """根据当前时间偏移计算出去年的日期

        Returns:
            DateTime: 去年
        """
        return self.offset_year(-1)

    def next_year(self):
        """根据当前时间偏移计算出明年的日期

        Returns:
            DateTime: 明年
        """
        return self.offset_year(1)

    def last_quarter(self):
        """根据当前时间偏移计算出上个季度的日期

        Returns:
            DateTime: 上个季度
        """
        return self.offset_quarter(-1)

    def next_quarter(self):
        """根据当前时间偏移计算出下个季度的日期

        Returns:
            DateTime: 下个季度
        """
        return self.offset_quarter(1)

    def last_month(self):
        """根据当前时间偏移计算出上个月的日期

        Returns:
            DateTime: 上个月
        """
        return self.offset_month(-1)

    def next_month(self):
        """根据当前时间偏移计算出下个月的日期

        Returns:
            DateTime: 下个月
        """
        return self.offset_month(1)

    def last_week(self):
        """根据当前时间偏移计算出上周的日期

        Returns:
            DateTime: 上周
        """
        return self.offset_week(-1)

    def next_week(self):
        """根据当前时间偏移计算出下周的日期

        Returns:
            DateTime: 下周
        """
        return self.offset_week(1)

    def yesterday(self):
        """根据当前时间偏移计算出昨天的日期

        Returns:
            DateTime: 昨天
        """
        return self.offset_day(-1)

    def tomorrow(self):
        """根据当前时间偏移计算出明天的日期

        Returns:
            DateTime: 明天
        """
        return self.offset_day(1)

    def offset_year(self, offset: int):
        """根据当前时间偏移计算出偏移后的日期

        Args:
            offset (int): 偏移量

        Returns:
            DateTime: 偏移后的日期
        """
        dt = self.datetime() + relativedelta(years=offset)
        self.__init__(
            dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond
        )
        return self

    def offset_quarter(self, offset: int):
        """根据当前时间偏移计算出偏移后的日期

        Args:
            offset (int): 偏移量

        Returns:
            DateTime: 偏移后的日期
        """
        dt = self.datetime() + relativedelta(months=offset * 3)
        self.__init__(
            dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond
        )
        return self

    def offset_month(self, offset: int):
        """根据当前时间偏移计算出偏移后的日期

        Args:
            offset (int): 偏移量

        Returns:
            DateTime: 偏移后的日期
        """
        dt = self.datetime() + relativedelta(months=offset)
        self.__init__(
            dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond
        )
        return self

    def offset_week(self, offset: int):
        """根据当前时间偏移计算出偏移后的日期

        Args:
            offset (int): 偏移量

        Returns:
            DateTime: 偏移后的日期
        """
        dt = self.datetime() + relativedelta(days=offset * 7)
        self.__init__(
            dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond
        )
        return self

    def offset_day(self, offset: int):
        """根据当前时间偏移计算出偏移后的日期

        Args:
            offset (int): 偏移量

        Returns:
            DateTime: 偏移后的日期
        """
        dt = self.datetime() + relativedelta(days=offset)
        self.__init__(
            dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond
        )
        return self

    def begin_of_year(self):
        """根据当前时间偏移计算出一年开始的日期

        Returns:
            DateTime: 一年的开始日期
        """
        self.__init__(self.year)
        return self

    def end_of_year(self):
        """根据当前时间偏移计算出一年结束的日期

        Returns:
            DateTime: 一年的结束日期
        """
        self.__init__(self.year, 12, 31, 23, 59, 59, 999999)
        return self

    def begin_of_quarter(self):
        """根据当前时间偏移计算出一季度开始的日期

        Returns:
            DateTime: 一季度的开始日期
        """
        if self.mon in [1, 2, 3]:
            m = 1
        elif self.mon in [4, 5, 6]:
            m = 4
        elif self.mon in [7, 8, 9]:
            m = 7
        else:
            m = 10
        self.__init__(self.year, m, 1)
        return self

    def end_of_quarter(self):
        """根据当前时间偏移计算出一季度结束的日期

        Returns:
            DateTime: 一季度的结束日期
        """

        self.begin_of_quarter()
        last_mon = self.mon + (3 - 1)
        last_day = calendar.monthrange(self.year, last_mon)[1]
        self.__init__(self.year, last_mon, last_day, 23, 59, 59, 999999)
        return self

    def begin_of_month(self):
        """根据当前时间偏移计算出一月开始的日期

        Returns:
            DateTime: 一月的开始日期
        """
        self.__init__(self.year, self.mon, 1)
        return self

    def end_of_month(self):
        """根据当前时间偏移计算出一月结束的日期

        Returns:
            DateTime: 一月的结束日期
        """
        last_day = calendar.monthrange(self.year, self.mon)[1]
        self.__init__(self.year, self.mon, last_day, 23, 59, 59, 999999)
        return self

    def begin_of_week(self):
        """根据当前时间偏移计算出一周开始的日期

        Returns:
            DateTime: 一周的开始日期
        """
        index_of_week = self.datetime().weekday()
        dt = self.offset_day(-index_of_week)
        self.__init__(dt.year, dt.mon, dt.day)
        return self

    def end_of_week(self):
        """根据当前时间偏移计算出一周结束的日期

        Returns:
            DateTime: 一周的结束日期
        """
        index_of_week = self.datetime().weekday()
        dt = self.offset_day(7 - (index_of_week + 1))
        self.__init__(dt.year, dt.mon, dt.day, 23, 59, 59, 999999)
        return self

    def begin_of_day(self):
        """根据当前时间偏移计算出一天开始的日期

        Returns:
            DateTime: 一天的开始日期
        """
        self.__init__(self.year, self.mon, self.day)
        return self

    def end_of_day(self):
        """根据当前时间偏移计算出一天结束的日期

        Returns:
            DateTime: 一天的结束日期
        """
        self.__init__(self.year, self.mon, self.day, 23, 59, 59, 999999)
        return self

    def datetime(self):
        return datetime(
            self.year, self.mon, self.day, self.hour, self.min, self.sec, self.millis
        )


class DateBetween(List[DateTime]):
    def __init__(self, begin: DateTime, end: DateTime):
        super().__init__()
        self.append(begin)
        self.append(end)
