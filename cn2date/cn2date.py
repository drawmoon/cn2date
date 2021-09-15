import cn2an

from datetime import datetime
from dateutil.relativedelta import relativedelta
from lark import Lark, Visitor, Tree, Token
from typing import Dict, List, Optional


def now():
    # 方便进行单元测试
    return datetime(2021, 9, 1)


class DateTreeVisitor(Visitor):
    date_dict: Dict[str, str]
    comb_part: Optional[str]
    cn_word_part: Optional[str]

    def __init__(self):
        self.date_dict = {}
        self.comb_part = None
        self.cn_word_part = None

    def years(self, tree: Tree):
        self.date_dict["year"] = self.__scan_values__(tree)

    def months(self, tree: Tree):
        today = now()
        keys = self.date_dict.keys()
        if "year" not in keys:
            self.date_dict["year"] = str(today.year)
        self.date_dict["month"] = self.__scan_values__(tree)

    def days(self, tree: Tree):
        today = now()
        keys = self.date_dict.keys()
        if "year" not in keys:
            self.date_dict["year"] = str(today.year)
        if "month" not in keys:
            self.date_dict["month"] = str(today.month).rjust(2, "0")
        self.date_dict["day"] = self.__scan_values__(tree)

    def comb(self, tree: Tree):
        self.comb_part = self.__scan_values__(tree)

    def cn_word(self, tree: Tree):
        self.cn_word_part = self.__scan_values__(tree)

    @staticmethod
    def __scan_values__(tree: Tree):
        val = ""
        for child in tree.children:
            if not isinstance(child, Token):
                raise TypeError("子节点不是 Token")
            val += child.value
        return val


class CnWordProcessor:
    synonym_dict: Dict[str, List[str]] = {"本": ["当前", "这个"]}

    def __init__(self, synonym: Optional[Dict[str, List[str]]] = None):
        if synonym is not None:
            self.synonym_dict = dict(self.synonym_dict, **synonym)

    def process(self, s: str):
        # 处理代名词
        if self.synonym_dict is not None:
            for k, synonyms in self.synonym_dict.items():
                for synonym in synonyms:
                    s = s.replace(synonym, k)
        if hasattr(self, s):
            fn = getattr(self, s)
            return fn()


# noinspection PyPep8Naming,NonAsciiCharacters
class YearCnWordProcessor(CnWordProcessor):
    def __init__(self):
        synonym = {"今": ["本"]}
        super(YearCnWordProcessor, self).__init__(synonym)

    @staticmethod
    def 今年():
        time = now()
        return build_date(time.year)

    @staticmethod
    def 明年():
        time = now()
        time += relativedelta(years=1)
        return build_date(time.year)

    @staticmethod
    def 去年():
        time = now()
        time -= relativedelta(years=1)
        return build_date(time.year)

    @staticmethod
    def 前年():
        time = now()
        time -= relativedelta(years=2)
        return build_date(time.year)

    @staticmethod
    def 上半年():
        today = now()
        start_date = datetime(today.year, 1, 1)
        end_date = datetime(today.year, 7, 1)
        return [start_date, end_date]

    @staticmethod
    def 下半年():
        today = now()
        start_date = datetime(today.year, 7, 1)
        today += relativedelta(years=1)
        end_date = datetime(today.year, 1, 1)
        return [start_date, end_date]


# noinspection PyPep8Naming,NonAsciiCharacters
class MonthCnWordProcessor(CnWordProcessor):
    @staticmethod
    def 本月():
        time = now()
        return build_date(month=time.month)

    @staticmethod
    def 下月():
        time = now()
        time += relativedelta(months=1)
        return build_date(month=time.month)

    @staticmethod
    def 上月():
        time = now()
        time -= relativedelta(months=1)
        return build_date(month=time.month)


# noinspection PyPep8Naming,NonAsciiCharacters
class DayCnWordProcessor(CnWordProcessor):
    def __init__(self):
        synonym = {"天": ["日"]}
        super(DayCnWordProcessor, self).__init__(synonym)

    @staticmethod
    def 今天():
        time = now()
        return build_date(time.year, time.month, time.day)

    @staticmethod
    def 明天():
        time = now()
        time += relativedelta(days=1)
        return build_date(time.year, time.month, time.day)

    @staticmethod
    def 后天():
        time = now()
        time += relativedelta(days=2)
        return build_date(time.year, time.month, time.day)

    @staticmethod
    def 昨天():
        time = now()
        time -= relativedelta(days=1)
        return build_date(time.year, time.month, time.day)

    @staticmethod
    def 前天():
        time = now()
        time -= relativedelta(days=2)
        return build_date(time.year, time.month, time.day)

    @staticmethod
    def 上午():
        time = now()
        start_date = datetime(time.year, time.month, time.day)
        end_date = start_date.replace(hour=12)
        return [start_date, end_date]

    @staticmethod
    def 下午():
        time = now()
        start_date = datetime(time.year, time.month, time.day, 12)
        end_date = start_date.replace(hour=19)
        return [start_date, end_date]


# noinspection PyPep8Naming,NonAsciiCharacters
class QuarterCnWordProcessor(CnWordProcessor):
    def __init__(self):
        synonym = {"一": ["1"], "二": ["2"], "三": ["3"], "四": ["4"]}
        super(QuarterCnWordProcessor, self).__init__(synonym)

    def 本季度(self):
        today = now()
        cur_quarter = (today.month - 1) // 3 + 1
        return self.process(f"{cur_quarter}季度")

    def 上季度(self):
        today = now()
        today -= relativedelta(months=3)
        cur_quarter = (today.month - 1) // 3 + 1
        return self.process(f"{cur_quarter}季度")

    def 下季度(self):
        today = now()
        today += relativedelta(months=3)
        cur_quarter = (today.month - 1) // 3 + 1
        return self.process(f"{cur_quarter}季度")

    @staticmethod
    def 一季度():
        today = now()
        start_date = datetime(today.year, 1, 1)
        end_date = datetime(today.year, 4, 1)
        return [start_date, end_date]

    @staticmethod
    def 二季度():
        today = now()
        start_date = datetime(today.year, 4, 1)
        end_date = datetime(today.year, 7, 1)
        return [start_date, end_date]

    @staticmethod
    def 三季度():
        today = now()
        start_date = datetime(today.year, 7, 1)
        end_date = datetime(today.year, 10, 1)
        return [start_date, end_date]

    @staticmethod
    def 四季度():
        today = now()
        start_date = datetime(today.year, 10, 1)
        today += relativedelta(years=1)
        end_date = datetime(today.year, 1, 1)
        return [start_date, end_date]


# noinspection PyPep8Naming,NonAsciiCharacters
class WeekCnWordProcessor(CnWordProcessor):
    def __init__(self):
        synonym = {"周": ["星期"]}
        super(WeekCnWordProcessor, self).__init__(synonym)

    @staticmethod
    def 本周():
        time = now()
        start_date = time - relativedelta(days=time.weekday())
        time += relativedelta(weeks=1)
        end_date = time - relativedelta(days=time.weekday())
        return [start_date, end_date]

    @staticmethod
    def 上周():
        time = now()
        last_week = time - relativedelta(weeks=1)
        start_date = last_week - relativedelta(days=last_week.weekday())
        end_date = time - relativedelta(days=time.weekday())
        return [start_date, end_date]

    @staticmethod
    def 下周():
        time = now() + relativedelta(weeks=1)
        start_date = time - relativedelta(days=time.weekday())
        time += relativedelta(weeks=1)
        end_date = time - relativedelta(days=time.weekday())
        return [start_date, end_date]


def str2digit(s, typ):
    opt = cn2an.transform(s)
    if not opt.isdigit():
        raise TypeError("字符转换为数字失败")
    if typ == "year":
        if len(opt) == 2:
            opt = str(now().year)[0:2] + opt
    return int(opt)


def build_date(year: int = None, month: int = None, day: int = None):
    if day is not None:
        start_date = datetime(year, month, day)
        end_date = start_date + relativedelta(days=1)
        return [start_date, end_date]
    if year is None and month is not None:
        today = now()
        start_date = datetime(today.year, month, 1)
        end_date = start_date + relativedelta(months=1)
        return [start_date, end_date]
    if year is not None and month is not None:
        start_date = datetime(year, month, 1)
        end_date = start_date + relativedelta(months=1)
        return [start_date, end_date]
    if year is not None:
        start_date = datetime(year, 1, 1)
        end_date = start_date + relativedelta(years=1)
        return [start_date, end_date]
    return []


def process_cn_word(dt_str):
    processor: CnWordProcessor
    if "年" in dt_str:
        processor = YearCnWordProcessor()
    elif "季度" in dt_str:
        processor = QuarterCnWordProcessor()
    elif "月" in dt_str:
        processor = MonthCnWordProcessor()
    elif "周" in dt_str or "星期" in dt_str:
        processor = WeekCnWordProcessor()
    elif "天" in dt_str or "日" in dt_str or "午" in dt_str:
        processor = DayCnWordProcessor()
    else:
        return []
    rst = processor.process(dt_str)
    return [] if rst is None else rst


def process_comb_date(date_lst: List[datetime], comb_str: str):
    comb_rst = process_cn_word(comb_str)
    if len(comb_rst) == 0:
        pass
    rst = []
    for i, dt in enumerate(date_lst):
        rpc_date = comb_rst[i]
        rst.append(dt.replace(month=rpc_date.month, day=rpc_date.day))
    if comb_rst[0].year == comb_rst[1].year:
        rst[1] = rst[1].replace(year=rst[0].year)
    return rst


date_grammar = r"""
    start: date | cn_word
    
    date   : ((years? months)? days) "当天"? | years? months? | (years | months) comb
    cn_word: "第"? (WORD | WORD WORD)? DIGIT? "个"? UNIT ("份" | "度" | "以" | "之")? WORD?
    
    years : DIGIT DIGIT (DIGIT DIGIT)? ("年" | "-" | "/")
    months: DIGIT DIGIT? ("月" | "月份" | "-" | "/")
    days  : DIGIT (DIGIT DIGIT?)? ("日" | "号")?
    comb  : COMD | "第"? DIGIT "个"? UNIT
    
    COMD : "上半年" | "下半年"
    WORD : "今" | "本" | "这个" | "当前" | "明" | "后" | "昨" | "上" | "下" | "前" | "后" | "内" | "去" | "半"
    UNIT : "年" | "季度" | "月" | "周" | "星期" | "天" | "日" | "午"
    DIGIT: /["0-9零一二两三四五六七八九十"]/
    
    // Disregard spaces in text
    %ignore " "
"""


def parse(dt_str):
    tree = Lark(date_grammar).parse(dt_str)
    visitor = DateTreeVisitor()
    visitor.visit(tree)

    if visitor.cn_word_part is not None:
        rst = process_cn_word(visitor.cn_word_part)
        return tuple([s.strftime("%Y-%m-%d %H:%M:%S") for s in rst])

    params = {}
    for key, val in visitor.date_dict.items():
        digit = str2digit(val, key)
        if digit is not None:
            params[key] = digit
    rst = build_date(**params)
    if visitor.comb_part is not None:
        rst = process_comb_date(rst, visitor.comb_part)
    return None if len(rst) == 0 else tuple([s.strftime("%Y-%m-%d %H:%M:%S") for s in rst])
