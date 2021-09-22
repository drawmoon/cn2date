from typing import Dict, List, Optional, Union
from dateutil.relativedelta import relativedelta

from cn2date.util import now, build_date


class CnWordProcessor:
    synonym_dict: Dict[str, List[str]] = {"本": ["当前", "这个"], "内": ["以来"]}

    def __init__(self, synonym: Optional[Dict[str, List[str]]] = None):
        if synonym is not None:
            self.synonym_dict = dict(self.synonym_dict, **synonym)

    def process(self, s: str, *args):
        # 处理代名词
        if self.synonym_dict is not None:
            for k, synonyms in self.synonym_dict.items():
                for synonym in synonyms:
                    s = s.replace(synonym, k)
        try:
            fn = getattr(self, s)
            return fn(*args) if len(args) > 0 else fn()
        except AttributeError:
            return []


# noinspection PyPep8Naming,NonAsciiCharacters
class YearCnWordProcessor(CnWordProcessor):
    def __init__(self):
        synonym = {"今": ["本"], "去年": ["上年"], "明年": ["下年"]}
        super(YearCnWordProcessor, self).__init__(synonym)

    _this_year = now().replace(month=1, day=1)

    def 今年(self):
        return build_date(self._this_year.year)

    def 明年(self):
        next_year = self._this_year + relativedelta(years=1)
        return build_date(next_year.year)

    def 去年(self):
        last_year = self._this_year - relativedelta(years=1)
        return build_date(last_year.year)

    def 前年(self):
        year_before_last = self._this_year - relativedelta(years=2)
        return build_date(year_before_last.year)

    def 上半年(self):
        start_date = self._this_year
        end_date = self._this_year.replace(month=7)
        return [start_date, end_date]

    def 下半年(self):
        start_date = self._this_year.replace(month=7)
        end_date = self._this_year + relativedelta(years=1)
        return [start_date, end_date]

    def 前几年(self, n: int):
        """
        例如 当前时间 2021/1/1，前三年，即 2018/1/1 - 2021/1/1
        """
        start_date = self._this_year - relativedelta(years=n)
        end_date = self._this_year
        return [start_date, end_date]

    def 后几年(self, n: int):
        """
        例如 当前时间 2021/1/1，后三年，即 2022/1/1 - 2025/1/1
        """
        start_date = self._this_year + relativedelta(years=1)
        end_date = start_date + relativedelta(years=n)
        return [start_date, end_date]

    def 几年前(self, n: int):
        """
        例如 当前时间 2021/1/1，三年前，即 2018/1/1 - 2019/1/1
        """
        start_date = self._this_year - relativedelta(years=n)
        end_date = start_date + relativedelta(years=1)
        return [start_date, end_date]

    def 几年后(self, n: int):
        """
        例如 当前时间 2021/1/1，三年后，即 2024/1/1 - 2025/1/1
        """
        start_date = self._this_year + relativedelta(years=n)
        end_date = start_date + relativedelta(years=1)
        return [start_date, end_date]

    def 几年内(self, n: int):
        """
        例如 当前时间 2021/1/1，三年内，即 2019/1/1 - 2022/1/1
        """
        start_date = self._this_year - relativedelta(years=(n - 1))
        end_date = self._this_year + relativedelta(years=1)
        return [start_date, end_date]


# noinspection PyPep8Naming,NonAsciiCharacters
class MonthCnWordProcessor(CnWordProcessor):
    _this_month = now().replace(day=1)

    def 本月(self):
        return build_date(self._this_month.year, self._this_month.month)

    def 下月(self):
        next_month = self._this_month + relativedelta(months=1)
        return build_date(next_month.year, next_month.month)

    def 上月(self):
        last_month = self._this_month - relativedelta(months=1)
        return build_date(last_month.year, last_month.month)

    def 前几月(self, n: int):
        """
        例如 当前时间 2021/10/1，前三月，即 2021/7/1 - 2021/10/1
        """
        start_date = self._this_month - relativedelta(months=n)
        end_date = self._this_month
        return [start_date, end_date]

    def 后几月(self, n: int):
        """
        例如 当前时间 2021/10/1，后三月，即 2021/11/1 - 2022/2/1
        """
        start_date = self._this_month + relativedelta(months=1)
        end_date = start_date + relativedelta(months=n)
        return [start_date, end_date]

    def 几月前(self, n: int):
        """
        例如 当前时间 2021/10/1，三月前，即 2021/7/1 - 2021/8/1
        """
        start_date = self._this_month - relativedelta(months=n)
        end_date = start_date + relativedelta(months=1)
        return [start_date, end_date]

    def 几月后(self, n: int):
        """
        例如 当前时间 2021/10/1，三月后，即 2022/1/1 - 2022/2/1
        """
        start_date = self._this_month + relativedelta(months=n)
        end_date = start_date + relativedelta(months=1)
        return [start_date, end_date]

    def 几月内(self, n: int):
        """
        例如 当前时间 2021/10/1，三月内，即 2021/8/1 - 2021/11/1
        """
        start_date = self._this_month - relativedelta(months=(n - 1))
        end_date = self._this_month + relativedelta(months=1)
        return [start_date, end_date]


# noinspection PyPep8Naming,NonAsciiCharacters
class DayCnWordProcessor(CnWordProcessor):
    def __init__(self):
        synonym = {"天": ["日"]}
        super(DayCnWordProcessor, self).__init__(synonym)

    _today = now()

    def 今天(self):
        return build_date(self._today.year, self._today.month, self._today.day)

    def 明天(self):
        next_day = self._today + relativedelta(days=1)
        return build_date(next_day.year, next_day.month, next_day.day)

    def 后天(self):
        day_after_tomorrow = self._today + relativedelta(days=2)
        return build_date(day_after_tomorrow.year, day_after_tomorrow.month, day_after_tomorrow.day)

    def 昨天(self):
        yesterday = self._today - relativedelta(days=1)
        return build_date(yesterday.year, yesterday.month, yesterday.day)

    def 前天(self):
        day_before_yesterday = self._today - relativedelta(days=2)
        return build_date(day_before_yesterday.year, day_before_yesterday.month, day_before_yesterday.day)

    def 上午(self):
        start_date = self._today
        end_date = start_date.replace(hour=12)
        return [start_date, end_date]

    def 下午(self):
        start_date = self._today.replace(hour=12)
        end_date = start_date.replace(hour=19)
        return [start_date, end_date]

    def 前几天(self, n: int):
        """
        例如 当前时间 2021/10/1，前三天，即 2021/9/28 - 2021/10/1
        """
        start_date = self._today - relativedelta(days=n)
        end_date = self._today
        return [start_date, end_date]

    def 后几天(self, n: int):
        """
        例如 当前时间 2021/10/1，后三天，即 2021/10/2 - 2021/10/5
        """
        start_date = self._today + relativedelta(days=1)
        end_date = start_date + relativedelta(days=n)
        return [start_date, end_date]

    def 几天前(self, n: int):
        """
        例如 当前时间 2021/10/1，三天前，即 2021/9/28 - 2021/9/29
        """
        start_date = self._today - relativedelta(days=n)
        end_date = start_date + relativedelta(days=1)
        return [start_date, end_date]

    def 几天后(self, n: int):
        """
        例如 当前时间 2021/10/1，三天后，即 2021/10/4 - 2021/10/5
        """
        start_date = self._today + relativedelta(days=n)
        end_date = start_date + relativedelta(days=1)
        return [start_date, end_date]

    def 几天内(self, n: int):
        """
        例如 当前时间 2021/10/1，三天内，即 2021/9/29 - 2021/10/2
        """
        start_date = self._today - relativedelta(days=(n - 1))
        end_date = self._today + relativedelta(days=1)
        return [start_date, end_date]


# noinspection PyPep8Naming,NonAsciiCharacters
class QuarterCnWordProcessor(CnWordProcessor):
    def __init__(self):
        synonym = {"一": ["1"], "二": ["2"], "三": ["3"], "四": ["4"]}
        super(QuarterCnWordProcessor, self).__init__(synonym)

    _this_month = now().replace(day=1)

    @staticmethod
    def _get_quarter(month: int):
        return (month - 1) // 3 + 1

    def process(self, s: str, *args):
        if len(s) == 1 and s.isdigit():
            s += "季度"
        return super(QuarterCnWordProcessor, self).process(s, *args)

    def 本季度(self):
        this_quarter = self._get_quarter(self._this_month.month)
        return self.process(str(this_quarter))

    def 上季度(self):
        month_of_last_quarter = self._this_month - relativedelta(months=3)
        last_quarter = self._get_quarter(month_of_last_quarter.month)
        return self.process(str(last_quarter))

    def 下季度(self):
        month_of_next_quarter = self._this_month + relativedelta(months=3)
        next_quarter = self._get_quarter(month_of_next_quarter.month)
        return self.process(str(next_quarter))

    def 一季度(self):
        start_date = self._this_month.replace(month=1)
        end_date = self._this_month.replace(month=4)
        return [start_date, end_date]

    def 二季度(self):
        start_date = self._this_month.replace(month=4)
        end_date = self._this_month.replace(month=7)
        return [start_date, end_date]

    def 三季度(self):
        start_date = self._this_month.replace(month=7)
        end_date = self._this_month.replace(month=10)
        return [start_date, end_date]

    def 四季度(self):
        start_date = self._this_month.replace(month=10)
        end_date = self._this_month.replace(month=1) + relativedelta(years=1)
        return [start_date, end_date]

    def 前几季度(self, n: int):
        """
        例如 当前时间 2021/10/1，前两季度，即 2021/4/1 - 2021/10/1
        """
        this_quarter = self.本季度()[0]
        start_date = this_quarter - relativedelta(months=(n * 3))
        end_date = this_quarter
        return [start_date, end_date]

    def 后几季度(self, n: int):
        """
        例如 当前时间 2021/10/1，后两季度，即 2022/1/1 - 2022/7/1
        """
        this_quarter = self.本季度()[0]
        start_date = this_quarter + relativedelta(months=3)
        end_date = start_date + relativedelta(months=(n * 3))
        return [start_date, end_date]

    def 几季度前(self, n: int):
        """
        例如 当前时间 2021/10/1，两季度前，即 2021/4/1 - 2021/7/1
        """
        this_quarter = self.本季度()[0]
        start_date = this_quarter - relativedelta(months=(n * 3))
        end_date = start_date + relativedelta(months=3)
        return [start_date, end_date]

    def 几季度后(self, n: int):
        """
        例如 当前时间 2021/10/1，两季度后，即 2022/4/1 - 2022/7/1
        """
        this_quarter = self.本季度()[0]
        start_date = this_quarter + relativedelta(months=(n * 3))
        end_date = start_date + relativedelta(months=3)
        return [start_date, end_date]

    def 几季度内(self, n: int):
        """
        例如 当前时间 2021/10/1，两季度内，即 2021/7/1 - 2022/1/1
        """
        this_quarter = self.本季度()[0]
        start_date = this_quarter - relativedelta(months=((n - 1) * 3))
        end_date = this_quarter + relativedelta(months=3)
        return [start_date, end_date]


# noinspection PyPep8Naming,NonAsciiCharacters
class WeekCnWordProcessor(CnWordProcessor):
    def __init__(self):
        synonym = {"周": ["星期"]}
        super(WeekCnWordProcessor, self).__init__(synonym)

    _today = now()
    # 计算出本周第一天
    _first_day_of_this_week = _today - relativedelta(days=_today.weekday())

    def 本周(self):
        start_date = self._first_day_of_this_week
        end_date = start_date + relativedelta(weeks=1)
        return [start_date, end_date]

    def 上周(self):
        start_date = self._first_day_of_this_week - relativedelta(weeks=1)
        end_date = self._first_day_of_this_week
        return [start_date, end_date]

    def 下周(self):
        start_date = self._first_day_of_this_week + relativedelta(weeks=1)
        end_date = start_date + relativedelta(weeks=1)
        return [start_date, end_date]

    def 前几周(self, n: int):
        """
        例如 当前时间 2021/10/1，前三周，即 2021/9/6 - 2021/9/27
        """
        start_date = self._first_day_of_this_week - relativedelta(weeks=n)
        end_date = self._first_day_of_this_week
        return [start_date, end_date]

    def 后几周(self, n: int):
        """
        例如 当前时间 2021/10/1，后三周，即 2021/10/4 - 2021/10/25
        """
        start_date = self._first_day_of_this_week + relativedelta(weeks=1)
        end_date = start_date + relativedelta(weeks=n)
        return [start_date, end_date]

    def 几周前(self, n: int):
        """
        例如 当前时间 2021/10/1，三周前，即 2021/9/6 - 2021/9/13
        """
        start_date = self._first_day_of_this_week - relativedelta(weeks=n)
        end_date = start_date + relativedelta(weeks=1)
        return [start_date, end_date]

    def 几周后(self, n: int):
        """
        例如 当前时间 2021/10/1，三周后，即 2021/10/18 - 2021/10/25
        """
        start_date = self._first_day_of_this_week + relativedelta(weeks=n)
        end_date = start_date + relativedelta(weeks=1)
        return [start_date, end_date]

    def 几周内(self, n: int):
        """
        例如 当前时间 2021/10/1，三周内，即 2021/9/13 - 2021/10/4
        """
        start_date = self._first_day_of_this_week - relativedelta(weeks=(n - 1))
        end_date = self._first_day_of_this_week + relativedelta(weeks=1)
        return [start_date, end_date]


def create_processor(inputs: str) -> CnWordProcessor:
    processor: Union[CnWordProcessor, None] = None

    if "年" in inputs:
        processor = YearCnWordProcessor()
    elif "季度" in inputs:
        processor = QuarterCnWordProcessor()
    elif "月" in inputs:
        processor = MonthCnWordProcessor()
    elif "周" in inputs or "星期" in inputs:
        processor = WeekCnWordProcessor()
    elif "天" in inputs or "日" in inputs or "午" in inputs:
        processor = DayCnWordProcessor()

    return processor
