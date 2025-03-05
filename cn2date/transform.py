import re
from datetime import datetime
from typing import Any, Dict, Optional

from cn2an import transform as cn2anTransform
from lark import Lark, ParseError, Transformer, UnexpectedCharacters

from .conf import (
    CN_ALIAS,
    DAY_ALIAS,
    MONTH_ALIAS,
    QUARTER_ALIAS,
    WEEK_ALIAS,
    YEAR_ALIAS,
)
from .datetime import DateBetween, DateTime


class TransformOptions:
    text: str
    transformer: Any
    lark: Optional[Lark]
    dt: Optional[DateTime]

    _defaults: Dict[str, Any]

    def __init__(self, options_dict: Dict[str, Any]):
        self._defaults = {"text": "", "lark": None, "transformer": None, "dt": None}

        for name, default in self._defaults.items():
            if name not in options_dict:
                setattr(self, name, default)
            else:
                setattr(self, name, options_dict[name])


def transform(s: str, **options: Dict[str, Any]) -> Optional[DateBetween]:
    try:
        o = TransformOptions(options)
        if o.transformer is None:
            raise TypeError("Transformer is not specified")
        o.text = s
        return o.transformer.transform(o)
    except UnexpectedCharacters:
        return None
    except ParseError:
        return None
    except Exception as e:
        raise e


# 常规日期格式转换器
class NormDateTransformer(Transformer):
    begin: Optional[DateTime]
    end: Optional[DateTime]

    def __init__(self):
        super().__init__()
        self.begin = DateTime(datetime.now().year, -1, -1)
        self.end = None

    def years(self, children):
        year_str = "".join(str(token) for token in children)
        if not year_str.isspace():
            year = int(cn2anTransform(year_str))
            year = (
                int(f"{str(datetime.now().year)[0:2]}{year}")
                if len(str(year)) == 2
                else year
            )
            self.begin.year = year

    def months(self, children):
        mon_str = "".join(str(token) for token in children)
        if not mon_str.isspace():
            mon = int(cn2anTransform(mon_str))
            self.begin.mon = mon

    def days(self, children):
        day_str = "".join(str(token) for token in children)
        if not day_str.isspace():
            day = int(cn2anTransform(day_str))
            self.begin.day = day

    def transform(self, options: TransformOptions) -> DateBetween:
        tree = options.lark.parse(options.text)
        self._transform_tree(tree)
        if self.begin.mon == -1 and self.begin.day == -1:
            self.begin.mon = 1
            self.begin.day = 1
            self.end = DateTime.of(self.begin).end_of_year()
        elif self.begin.day != -1:
            if self.begin.mon == -1:
                self.begin.mon = datetime.now().month
            self.end = DateTime.of(self.begin).end_of_day()
        else:
            if self.begin.day == -1:
                self.begin.day = 1
            self.end = DateTime.of(self.begin).end_of_month()
        return DateBetween(self.begin, self.end)


# 口语化日期格式转换器
class ChineDateTransformer(Transformer):
    begin: Optional[DateTime]
    end: Optional[DateTime]

    def __init__(self):
        super().__init__()
        self.begin = None
        self.end = None

    def _get_str(self, children, alias_dict) -> str:
        s = "".join(str(token) for token in children)
        for k, alias in alias_dict.items():
            if "," in alias:
                for a in alias.split(","):
                    s = s.replace(a, k)
            else:
                s = s.replace(alias, k)
        return s

    def years(self, children):
        s = self._get_str(children, {**CN_ALIAS, **YEAR_ALIAS})

        it = {
            "今年": DateTime.now().begin_of_year(),
            "明年": DateTime.now().begin_of_year().next_year(),
            "去年": DateTime.now().begin_of_year().last_year(),
            "前年": DateTime.now().begin_of_year().offset_year(-2),
            "下半年": DateTime(datetime.now().year, 7),
        }
        if s in it:
            self.begin = it[s]
            self.end = DateTime.of(self.begin).end_of_year()
        elif s == "上半年":
            self.begin = DateTime.now().begin_of_year()
            self.end = DateTime(datetime.now().year, 6, 30, 23, 59, 59, 999999)
        else:
            has_num_str = cn2anTransform(s)
            if re.search(r"\d", has_num_str):
                arg = int(re.findall(r"\d+", has_num_str)[0])
                if has_num_str.startswith("前"):
                    # 对“前几年”的句式的处理
                    # 比如当前时间是“2021/1/1”
                    # 前三年, 即“2018/1/1 00:00:00 - 2020/12/31 23:59:59”
                    self.begin = DateTime.now().begin_of_year().offset_year(-arg)
                    self.end = DateTime.now().offset_year(-1).end_of_year()
                elif has_num_str.startswith("后"):
                    # 对“后几年”的句式的处理
                    # 比如当前时间是“2021/1/1”
                    # 后三年, 即“2022/1/1 00:00:00 - 2024/12/31 23:59:59”
                    self.begin = DateTime.now().begin_of_year().offset_year(1)
                    self.end = (
                        DateTime.of(self.begin).offset_year(arg - 1).end_of_year()
                    )
                elif has_num_str.endswith("前"):
                    # 对“几年前”的句式的处理
                    # 比如当前时间是“2021/1/1”
                    # 三年前, 即“2018/1/1 00:00:00 - 2018/12/31 23:59:59”
                    self.begin = DateTime.now().begin_of_year().offset_year(-arg)
                    self.end = DateTime.of(self.begin).end_of_year()
                elif has_num_str.endswith("后"):
                    # 对“几年后”的句式的处理
                    # 比如当前时间是“2021/1/1”
                    # 三年后, 即“2024/1/1 00:00:00 - 2024/12/31 23:59:59”
                    self.begin = DateTime.now().begin_of_year().offset_year(arg)
                    self.end = DateTime.of(self.begin).end_of_year()
                elif has_num_str.endswith("内"):
                    # 对“几年内”的句式的处理
                    # 在没有明确指定“过去”、“未来”的时, 解释为过去式且包含今年
                    # 比如当前时间是“2021/1/1”
                    # 三年内, 即“2019/1/1 00:00:00 - 2021/12/31 23:59:59”
                    self.begin = DateTime.now().begin_of_year().offset_year(-(arg - 1))
                    self.end = DateTime.now().end_of_year()

    def quarters(self, children):
        s = self._get_str(children, {**CN_ALIAS, **QUARTER_ALIAS})

        it = {
            "本季度": DateTime.now().begin_of_quarter(),
            "上季度": DateTime.now().begin_of_quarter().last_quarter(),
            "下季度": DateTime.now().begin_of_quarter().next_quarter(),
            "1季度": DateTime(datetime.now().year, 1),
            "2季度": DateTime(datetime.now().year, 4),
            "3季度": DateTime(datetime.now().year, 7),
            "4季度": DateTime(datetime.now().year, 10),
        }
        if s in it:
            self.begin = it[s]
            self.end = DateTime.of(self.begin).end_of_quarter()
        else:
            has_num_str = cn2anTransform(s)
            if re.search(r"\d", has_num_str):
                if len(s) == 3 and s.endswith("季度") and has_num_str[0].isdigit():
                    self.begin = it[has_num_str]
                    self.end = DateTime.of(self.begin).end_of_quarter()
                else:
                    arg = int(re.findall(r"\d+", has_num_str)[0])
                    if has_num_str.startswith("前"):
                        # 对“前几季度”的句式的处理
                        # 比如当前时间是“2021/1/1”
                        # 前三季度, 即“2020/4/1 00:00:00 - 2020/12/31 23:59:59”
                        self.begin = (
                            DateTime.now().begin_of_quarter().offset_quarter(-arg)
                        )
                        self.end = DateTime.now().offset_quarter(-1).end_of_quarter()
                    elif has_num_str.startswith("后"):
                        # 对“后几季度”的句式的处理
                        # 比如当前时间是“2021/1/1”
                        # 后三季度, 即“2021/4/1 00:00:00 - 2021/12/31 23:59:59”
                        self.begin = DateTime.now().begin_of_quarter().offset_quarter(1)
                        self.end = (
                            DateTime.of(self.begin)
                            .offset_quarter(arg - 1)
                            .end_of_quarter()
                        )
                    elif has_num_str.endswith("前"):
                        # 对“几季度前”的句式的处理
                        # 比如当前时间是“2021/1/1”
                        # 三季度前, 即“2020/4/1 00:00:00 - 2020/6/30 23:59:59”
                        self.begin = (
                            DateTime.now().begin_of_quarter().offset_quarter(-arg)
                        )
                        self.end = DateTime.of(self.begin).end_of_quarter()
                    elif has_num_str.endswith("后"):
                        # 对“几季度后”的句式的处理
                        # 比如当前时间是“2021/1/1”
                        # 三季度后, 即“2021/10/1 00:00:00 - 2021/12/31 23:59:59”
                        self.begin = (
                            DateTime.now().begin_of_quarter().offset_quarter(arg)
                        )
                        self.end = DateTime.of(self.begin).end_of_quarter()
                    elif has_num_str.endswith("内"):
                        # 对“几季度内”的句式的处理
                        # 在没有明确指定“过去”、“未来”的时, 解释为过去式且包含今年
                        # 比如当前时间是“2021/1/1”
                        # 三季度内, 即“2020/7/1 00:00:00 - 2021/3/31 23:59:59”
                        self.begin = (
                            DateTime.now().begin_of_quarter().offset_quarter(-(arg - 1))
                        )
                        self.end = DateTime.now().end_of_quarter()

    def months(self, children):
        s = self._get_str(children, {**CN_ALIAS, **MONTH_ALIAS})

        it = {
            "本月": DateTime.now().begin_of_month(),
            "上月": DateTime.now().begin_of_month().last_month(),
            "下月": DateTime.now().begin_of_month().next_month(),
        }
        if s in it:
            self.begin = it[s]
            self.end = DateTime.of(self.begin).end_of_month()
        else:
            has_num_str = cn2anTransform(s)
            if re.search(r"\d", has_num_str):
                arg = int(re.findall(r"\d+", has_num_str)[0])
                if has_num_str.startswith("前"):
                    # 对“前几月”的句式的处理
                    # 比如当前时间是“2021/1/1”
                    # 前三月, 即“2020/10/1 00:00:00 - 2020/12/31 23:59:59”
                    self.begin = DateTime.now().begin_of_month().offset_month(-arg)
                    self.end = DateTime.now().offset_month(-1).end_of_month()
                elif has_num_str.startswith("后"):
                    # 对“后几月”的句式的处理
                    # 比如当前时间是“2021/1/1”
                    # 后三月, 即“2021/4/1 00:00:00 - 2021/4/30 23:59:59”
                    self.begin = DateTime.now().begin_of_month().offset_month(1)
                    self.end = (
                        DateTime.of(self.begin).offset_month(arg - 1).end_of_month()
                    )
                elif has_num_str.endswith("前"):
                    # 对“几月前”的句式的处理
                    # 比如当前时间是“2021/1/1”
                    # 三月前, 即“2020/10/1 00:00:00 - 2020/12/31 23:59:59”
                    self.begin = DateTime.now().begin_of_month().offset_month(-arg)
                    self.end = DateTime.of(self.begin).end_of_month()
                elif has_num_str.endswith("后"):
                    # 对“几月后”的句式的处理
                    # 比如当前时间是“2021/1/1”
                    # 三月后, 即“2021/2/1 00:00:00 - 2020/4/30 23:59:59”
                    self.begin = DateTime.now().begin_of_month().offset_month(arg)
                    self.end = DateTime.of(self.begin).end_of_month()
                elif has_num_str.endswith("内"):
                    # 对“几月内”的句式的处理
                    # 在没有明确指定“过去”、“未来”的时, 解释为过去式且包含今月
                    # 比如当前时间是“2021/1/1”
                    # 三月内, 即“2020/11/1 00:00:00 - 2021/1/31 23:59:59”
                    self.begin = (
                        DateTime.now().begin_of_month().offset_month(-(arg - 1))
                    )
                    self.end = DateTime.now().end_of_month()

    def weeks(self, children):
        s = self._get_str(children, {**CN_ALIAS, **WEEK_ALIAS})

        it = {
            "本周": DateTime.now().begin_of_week(),
            "上周": DateTime.now().begin_of_week().last_week(),
            "下周": DateTime.now().begin_of_week().next_week(),
        }
        if s in it:
            self.begin = it[s]
            self.end = DateTime.of(self.begin).end_of_week()
        else:
            has_num_str = cn2anTransform(s)
            if re.search(r"\d", has_num_str):
                arg = int(re.findall(r"\d+", has_num_str)[0])
                if has_num_str.startswith("前"):
                    # 对“前几周”的句式的处理
                    # 比如当前时间是“2021/1/1”
                    # 前三周, 即“2020/12/7 00:00:00 - 2020/12/27 23:59:59”
                    self.begin = DateTime.now().begin_of_week().offset_week(-arg)
                    self.end = DateTime.now().offset_week(-1).end_of_week()
                elif has_num_str.startswith("后"):
                    # 对“后几周”的句式的处理
                    # 比如当前时间是“2021/1/1”
                    # 后三周, 即“2021/1/4 00:00:00 - 2021/1/24 23:59:59”
                    self.begin = DateTime.now().begin_of_week().offset_week(1)
                    self.end = (
                        DateTime.of(self.begin).offset_week(arg - 1).end_of_week()
                    )
                elif has_num_str.endswith("前"):
                    # 对“几周前”的句式的处理
                    # 比如当前时间是“2021/1/1”
                    # 三周前, 即“2020/12/7 00:00:00 - 2020/12/13 23:59:59”
                    self.begin = DateTime.now().begin_of_week().offset_week(-arg)
                    self.end = DateTime.of(self.begin).end_of_week()
                elif has_num_str.endswith("后"):
                    # 对“几周后”的句式的处理
                    # 比如当前时间是“2021/1/1”
                    # 三周后, 即“2021/1/18 00:00:00 - 2021/1/24 23:59:59”
                    self.begin = DateTime.now().begin_of_week().offset_week(arg)
                    self.end = DateTime.of(self.begin).end_of_week()
                elif has_num_str.endswith("内"):
                    # 对“几周内”的句式的处理
                    # 在没有明确指定“过去”、“未来”的时, 解释为过去式且包含今年
                    # 比如当前时间是“2021/1/1”
                    # 三周内, 即“2020/12/14 00:00:00 - 2021/1/3 23:59:59”
                    self.begin = DateTime.now().begin_of_week().offset_week(-(arg - 1))
                    self.end = DateTime.now().end_of_week()

    def days(self, children):
        s = self._get_str(children, {**CN_ALIAS, **DAY_ALIAS})

        it = {
            "今天": DateTime.now().begin_of_day(),
            "明天": DateTime.now().begin_of_day().tomorrow(),
            "后天": DateTime.now().begin_of_day().offset_day(2),
            "昨天": DateTime.now().begin_of_day().yesterday(),
            "前天": DateTime.now().begin_of_day().offset_day(-2),
        }
        if s in it:
            self.begin = it[s]
            self.end = DateTime.of(self.begin).end_of_day()
        else:
            has_num_str = cn2anTransform(s)
            if re.search(r"\d", has_num_str):
                arg = int(re.findall(r"\d+", has_num_str)[0])
                if has_num_str.startswith("前"):
                    # 对“前几天”的句式的处理
                    # 比如当前时间是“2021/1/1”
                    # 前三天, 即“2021/9/28 00:00:00 - 2021/9/30 23:59:59”
                    self.begin = DateTime.now().begin_of_day().offset_day(-arg)
                    self.end = DateTime.now().offset_day(-1).end_of_day()
                elif has_num_str.startswith("后"):
                    # 对“后几天”的句式的处理
                    # 比如当前时间是“2021/1/1”
                    # 后三天, 即“2021/10/2 00:00:00 - 2021/10/4 23:59:59”
                    self.begin = DateTime.now().begin_of_day().offset_day(1)
                    self.end = DateTime.of(self.begin).offset_day(arg - 1).end_of_day()
                elif has_num_str.endswith("前"):
                    # 对“几天前”的句式的处理
                    # 比如当前时间是“2021/1/1”
                    # 三天前, 即“2021/9/28 00:00:00 - 2021/9/28 23:59:59”
                    self.begin = DateTime.now().begin_of_day().offset_day(-arg)
                    self.end = DateTime.of(self.begin).end_of_day()
                elif has_num_str.endswith("后"):
                    # 对“几天后”的句式的处理
                    # 比如当前时间是“2021/1/1”
                    # 三天后, 即“2021/10/4 00:00:00 - 2021/10/4 23:59:59”
                    self.begin = DateTime.now().begin_of_day().offset_day(arg)
                    self.end = DateTime.of(self.begin).end_of_day()
                elif has_num_str.endswith("内"):
                    # 对“几天内”的句式的处理
                    # 在没有明确指定“过去”、“未来”的时, 解释为过去式且包含今天
                    # 比如当前时间是“2021/1/1”
                    # 三天内, 即“2021/9/29 00:00:00 - 2021/10/1 23:59:59”
                    self.begin = DateTime.now().begin_of_day().offset_day(-(arg - 1))
                    self.end = DateTime.now().end_of_day()

    def long_time(self, children):
        s = self._get_str(children, CN_ALIAS)

        if s == "上午":
            n = datetime.now()
            self.begin = DateTime.of(n).begin_of_day()
            self.end = DateTime(n.year, n.month, n.day, 11, 59, 59, 999999)
        if s == "下午":
            n = datetime.now()
            self.begin = DateTime(n.year, n.month, n.day, 12)
            self.end = DateTime(n.year, n.month, n.day, 18, 59, 59, 999999)

    def transform(self, options: TransformOptions) -> DateBetween:
        # 上一个分词段落处理完成的日期, 如果是空, 那么它是第一个词
        if options.dt is not None:
            self.begin = options.dt

        tree = options.lark.parse(options.text)
        self._transform_tree(tree)
        return DateBetween(self.begin, self.end)
