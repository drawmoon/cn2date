from datetime import datetime
from typing import Any, Dict, Optional

from lark import Lark, Transformer, UnexpectedCharacters

from .conf import (
    CN_ALIAS,
    DAY_ALIAS,
    MONTH_ALIAS,
    NUMERAL_NUM2CN,
    QUARTER_ALIAS,
    WEEK_ALIAS,
    YEAR_ALIAS,
)
from .datetime import DateBetween, DateTime
from .util import cn2num


class TransformOptions:
    text: str
    transformer: Any
    lark: Optional[Lark]
    dt: Optional[DateTime]

    _defaults = {"text": "", "lark": None, "transformer": None, "dt": None}

    def __init__(self, options_dict: Dict[str, Any]):
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
            year = cn2num(year_str)
            year = (
                int(f"{str(datetime.now().year)[0:2]}{year}")
                if len(str(year)) == 2
                else year
            )
            self.begin.year = year

    def months(self, children):
        mon_str = "".join(str(token) for token in children)
        if not mon_str.isspace():
            mon = cn2num(mon_str)
            self.begin.mon = mon

    def days(self, children):
        day_str = "".join(str(token) for token in children)
        if not day_str.isspace():
            day = cn2num(day_str)
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
        return self.begin, self.end


# 口语化日期格式转换器
class ChineDateTransformer(Transformer):
    begin: Optional[DateTime]
    end: Optional[DateTime]

    def __init__(self):
        super().__init__()
        self.begin = None
        self.end = None

    def years(self, children):
        s = "".join(str(token) for token in children)
        for k, alias in {**CN_ALIAS, **YEAR_ALIAS}.items():
            if "," in alias:
                for a in alias.split(","):
                    s = s.replace(a, k)
            else:
                s = s.replace(alias, k)

        if s == "上半年":
            n = datetime.now()
            self.begin = DateTime.of(n).begin_of_year()
            self.end = DateTime(n.year, 6, 30, 23, 59, 59, 999999)
        elif s == "下半年":
            n = datetime.now()
            self.begin = DateTime(n.year, 7)
            self.end = DateTime.of(self.begin).end_of_year()
        else:
            it = {
                "今年": DateTime.of(datetime.now()).begin_of_year(),
                "明年": DateTime.of(datetime.now()).begin_of_year().next_year(),
                "去年": DateTime.of(datetime.now()).begin_of_year().last_year(),
                "前年": DateTime.of(datetime.now()).begin_of_year().offset_year(-2),
            }
            if s in it:
                self.begin = it[s]
            if self.begin is not None:
                self.end = DateTime.of(self.begin).end_of_year()

    def quarters(self, children):
        s = "".join(str(token) for token in children)
        for k, alias in {**CN_ALIAS, **QUARTER_ALIAS, **NUMERAL_NUM2CN}.items():
            if "," in alias:
                for a in alias.split(","):
                    s = s.replace(a, k)
            else:
                s = s.replace(alias, k)

        it = {
            "本季度": DateTime.of(datetime.now()).begin_of_quarter(),
            "上季度": DateTime.of(datetime.now()).begin_of_quarter().last_quarter(),
            "下季度": DateTime.of(datetime.now()).begin_of_quarter().next_quarter(),
            "1季度": DateTime(datetime.now().year, 1),
            "2季度": DateTime(datetime.now().year, 4),
            "3季度": DateTime(datetime.now().year, 7),
            "4季度": DateTime(datetime.now().year, 10),
        }
        if s in it:
            self.begin = it[s]
        if self.begin is not None:
            self.end = DateTime.of(self.begin).end_of_quarter()

    def months(self, children):
        s = "".join(str(token) for token in children)
        for k, alias in {**CN_ALIAS, **MONTH_ALIAS}.items():
            if "," in alias:
                for a in alias.split(","):
                    s = s.replace(a, k)
            else:
                s = s.replace(alias, k)

        it = {
            "本月": DateTime.of(datetime.now()).begin_of_month(),
            "上月": DateTime.of(datetime.now()).begin_of_month().last_month(),
            "下月": DateTime.of(datetime.now()).begin_of_month().next_month(),
        }
        if s in it:
            self.begin = it[s]
        if self.begin is not None:
            self.end = DateTime.of(self.begin).end_of_month()

    def weeks(self, children):
        s = "".join(str(token) for token in children)
        for k, alias in {**CN_ALIAS, **WEEK_ALIAS}.items():
            if "," in alias:
                for a in alias.split(","):
                    s = s.replace(a, k)
            else:
                s = s.replace(alias, k)

        it = {
            "本周": DateTime.of(datetime.now()).begin_of_week(),
            "上周": DateTime.of(datetime.now()).begin_of_week().last_week(),
            "下周": DateTime.of(datetime.now()).begin_of_week().next_week(),
        }
        if s in it:
            self.begin = it[s]
        if self.begin is not None:
            self.end = DateTime.of(self.begin).end_of_week()

    def days(self, children):
        s = "".join(str(token) for token in children)
        for k, alias in {**CN_ALIAS, **DAY_ALIAS}.items():
            if "," in alias:
                for a in alias.split(","):
                    s = s.replace(a, k)
            else:
                s = s.replace(alias, k)

        it = {
            "今天": DateTime.of(datetime.now()),
            "明天": DateTime.of(datetime.now()).tomorrow(),
            "后天": DateTime.of(datetime.now()).offset_day(2),
            "昨天": DateTime.of(datetime.now()).yesterday(),
            "前天": DateTime.of(datetime.now()).offset_day(-2),
        }
        if s in it:
            self.begin = it[s]
        if self.begin is not None:
            self.end = DateTime.of(self.begin).end_of_day()

    def long_time(self, children):
        s = "".join(str(token) for token in children)
        for k, alias in CN_ALIAS.items():
            if "," in alias:
                for a in alias.split(","):
                    s = s.replace(a, k)
            else:
                s = s.replace(alias, k)

        if s == "上午":
            n = datetime.now()
            self.begin = DateTime.of(n)
            self.end = DateTime(n.year, n.month, n.day, 11, 59, 59, 999999)
        if s == "下午":
            n = datetime.now()
            self.begin = DateTime(n.year, n.month, n.day, 12)
            self.end = DateTime(n.year, n.month, n.day, 18, 59, 59, 999999)

    def transform(self, options: TransformOptions) -> DateBetween:
        # 上一个分词段落处理完成的日期，如果是空，那么它是第一个词
        if options.dt is not None:
            self.begin = options.dt

        tree = options.lark.parse(options.text)
        self._transform_tree(tree)
        return self.begin, self.end
