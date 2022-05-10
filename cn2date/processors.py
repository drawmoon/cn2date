from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union

from lark import Lark, Visitor

from cn2date.util import date_add, date_sub, endof, now, startof


class Processor:
    def __init__(
        self,
        parser: Lark,
        visitor: Visitor,
        synonym: Optional[Dict[str, List[str]]] = None,
    ):
        self._parser = parser
        self._visitor = visitor
        self._synonym = synonym

    def process(self, text: str, *args) -> Tuple[datetime, datetime]:
        # 处理代名词
        if self._synonym is not None:
            for k, synonyms in self._synonym.items():
                for synonym in synonyms:
                    text = text.replace(synonym, k)


class HabitProcessor:
    synonym_dict: Dict[str, List[str]] = {
        "本": ["当前", "这个"],
        "内": ["以内", "之内"],
        "以前": ["之前"],
    }

    def __init__(self, synonym: Optional[Dict[str, List[str]]] = None):
        self.now = now()

        if synonym is not None:
            self.synonym_dict = dict(self.synonym_dict, **synonym)

    def process(self, text: str, *args) -> Tuple[datetime, datetime]:
        # 处理代名词
        if self.synonym_dict is not None:
            for k, synonyms in self.synonym_dict.items():
                for synonym in synonyms:
                    text = text.replace(synonym, k)

        try:
            fn = getattr(self, text)
            return fn(*args) if len(args) > 0 else fn()
        except AttributeError:
            raise ValueError(f"Can't parse the text: {text}")


# noinspection PyPep8Naming,NonAsciiCharacters
class YearProcessor(HabitProcessor):
    def __init__(self):
        synonym = {"今": ["本"], "去年": ["上年"], "明年": ["下年"]}
        super(YearProcessor, self).__init__(synonym)

    def 今年(self):
        s = startof(self.now, "y")
        e = endof(s, "y")
        return s, e

    def 明年(self):
        s = date_add(startof(self.now, "y"), 1, "y")
        e = endof(s, "y")
        return s, e

    def 去年(self):
        s = date_sub(startof(self.now, "y"), 1, "y")
        e = endof(s, "y")
        return s, e

    def 前年(self):
        s = date_sub(startof(self.now, "y"), 2, "y")
        e = endof(s, "y")
        return s, e

    def 上半年(self):
        s = startof(self.now, "fhoy")
        e = endof(s, "fhoy")
        return s, e

    def 下半年(self):
        s = startof(self.now, "shoy")
        e = endof(s, "shoy")
        return s, e

    def 前几年(self, n: int):
        """
        例如：当前时间 2021/1/1，前三年，即 2018/1/1 - 2021/1/1
        """
        s = date_sub(startof(self.now, "y"), n, "y")
        e = startof(self.now, "y")
        return s, e

    def 后几年(self, n: int):
        """
        例如：当前时间 2021/1/1，后三年，即 2022/1/1 - 2025/1/1
        """
        s = date_add(startof(self.now, "y"), 1, "y")
        e = date_add(s, n, "y")
        return s, e

    def 几年前(self, n: int):
        """
        例如：当前时间 2021/1/1，三年前，即 2018/1/1 - 2019/1/1
        """
        s = date_sub(startof(self.now, "y"), n, "y")
        e = endof(s, "y")
        return s, e

    def 几年后(self, n: int):
        """
        例如：当前时间 2021/1/1，三年后，即 2024/1/1 - 2025/1/1
        """
        s = date_add(startof(self.now, "y"), n, "y")
        e = endof(s, "y")
        return s, e

    def 几年内(self, n: int):
        """
        例如：当前时间 2021/1/1，三年内，即 2019/1/1 - 2022/1/1
        """
        s = date_sub(startof(self.now, "y"), n - 1, "y")
        e = date_add(startof(self.now, "y"), 1, "y")
        return s, e


# noinspection PyPep8Naming,NonAsciiCharacters
class QuarterProcessor(HabitProcessor):
    def __init__(self):
        synonym = {"一": ["1"], "二": ["2"], "三": ["3"], "四": ["4"]}
        super(QuarterProcessor, self).__init__(synonym)

    def process(self, s: str, *args):
        if len(s) == 1 and s.isdigit():
            s += "季度"
        return super(QuarterProcessor, self).process(s, *args)

    def 本季度(self):
        s = startof(self.now, "q")
        e = endof(s, "q")
        return s, e

    def 上季度(self):
        s = date_sub(startof(self.now, "q"), 1, "q")
        e = endof(s, "q")
        return s, e

    def 下季度(self):
        s = date_add(startof(self.now, "q"), 1, "q")
        e = endof(s, "q")
        return s, e

    def 一季度(self):
        s = startof(self.now, "fq")
        e = endof(s, "fq")
        return s, e

    def 二季度(self):
        s = startof(self.now, "sq")
        e = endof(s, "sq")
        return s, e

    def 三季度(self):
        s = startof(self.now, "tq")
        e = endof(s, "tq")
        return s, e

    def 四季度(self):
        s = startof(self.now, "foq")
        e = endof(s, "foq")
        return s, e

    def 前几季度(self, n: int):
        """
        例如：当前时间 2021/10/1，前两季度，即 2021/4/1 - 2021/10/1
        """
        s = date_sub(startof(self.now, "q"), n, "q")
        e = startof(self.now, "q")
        return s, e

    def 后几季度(self, n: int):
        """
        例如：当前时间 2021/10/1，后两季度，即 2022/1/1 - 2022/7/1
        """
        s = date_add(startof(self.now, "q"), 1, "q")
        e = date_add(s, n, "q")
        return s, e

    def 几季度前(self, n: int):
        """
        例如：当前时间 2021/10/1，两季度前，即 2021/4/1 - 2021/7/1
        """
        s = date_sub(startof(self.now, "q"), n, "q")
        e = endof(s, "q")
        return s, e

    def 几季度后(self, n: int):
        """
        例如：当前时间 2021/10/1，两季度后，即 2022/4/1 - 2022/7/1
        """
        s = date_add(startof(self.now, "q"), n, "q")
        e = endof(s, "q")
        return s, e

    def 几季度内(self, n: int):
        """
        例如：当前时间 2021/10/1，两季度内，即 2021/7/1 - 2022/1/1
        """
        s = date_sub(startof(self.now, "q"), n - 1, "q")
        e = date_add(startof(self.now, "q"), 1, "q")
        return s, e


# noinspection PyPep8Naming,NonAsciiCharacters
class MonthProcessor(HabitProcessor):
    def 本月(self):
        s = startof(self.now, "m")
        e = endof(s, "m")
        return s, e

    def 下月(self):
        s = date_add(startof(self.now, "m"), 1, "m")
        e = endof(s, "m")
        return s, e

    def 上月(self):
        s = date_sub(startof(self.now, "m"), 1, "m")
        e = endof(s, "m")
        return s, e

    def 前几月(self, n: int):
        """
        例如：当前时间 2021/10/1，前三月，即 2021/7/1 - 2021/10/1
        """
        s = date_sub(startof(self.now, "m"), n, "m")
        e = startof(self.now, "m")
        return s, e

    def 后几月(self, n: int):
        """
        例如：当前时间 2021/10/1，后三月，即 2021/11/1 - 2022/2/1
        """
        s = date_add(startof(self.now, "m"), 1, "m")
        e = date_add(s, n, "m")
        return s, e

    def 几月前(self, n: int):
        """
        例如：当前时间 2021/10/1，三月前，即 2021/7/1 - 2021/8/1
        """
        s = date_sub(startof(self.now, "m"), n, "m")
        e = endof(s, "m")
        return s, e

    def 几月后(self, n: int):
        """
        例如：当前时间 2021/10/1，三月后，即 2022/1/1 - 2022/2/1
        """
        s = date_add(startof(self.now, "m"), n, "m")
        e = endof(s, "m")
        return s, e

    def 几月内(self, n: int):
        """
        例如：当前时间 2021/10/1，三月内，即 2021/8/1 - 2021/11/1
        """
        s = date_sub(startof(self.now, "m"), n - 1, "m")
        e = date_add(startof(self.now, "m"), 1, "m")
        return s, e


# noinspection PyPep8Naming,NonAsciiCharacters
class WeekProcessor(HabitProcessor):
    def __init__(self):
        synonym = {"周": ["星期"]}
        super(WeekProcessor, self).__init__(synonym)

    def 本周(self):
        s = startof(self.now, "w")
        e = endof(s, "w")
        return s, e

    def 上周(self):
        s = date_sub(startof(self.now, "w"), 1, "w")
        e = endof(s, "w")
        return s, e

    def 下周(self):
        s = date_add(startof(self.now, "w"), 1, "w")
        e = endof(s, "w")
        return s, e

    def 前几周(self, n: int):
        """
        例如：当前时间 2021/10/1，前三周，即 2021/9/6 - 2021/9/27
        """
        s = date_sub(startof(self.now, "w"), n, "w")
        e = startof(self.now, "w")
        return s, e

    def 后几周(self, n: int):
        """
        例如：当前时间 2021/10/1，后三周，即 2021/10/4 - 2021/10/25
        """
        s = date_add(startof(self.now, "w"), 1, "w")
        e = date_add(s, n, "w")
        return s, e

    def 几周前(self, n: int):
        """
        例如：当前时间 2021/10/1，三周前，即 2021/9/6 - 2021/9/13
        """
        s = date_sub(startof(self.now, "w"), n, "w")
        e = endof(s, "w")
        return s, e

    def 几周后(self, n: int):
        """
        例如：当前时间 2021/10/1，三周后，即 2021/10/18 - 2021/10/25
        """
        s = date_add(startof(self.now, "w"), n, "w")
        e = endof(s, "w")
        return s, e

    def 几周内(self, n: int):
        """
        例如：当前时间 2021/10/1，三周内，即 2021/9/13 - 2021/10/4
        """
        s = date_sub(startof(self.now, "w"), n - 1, "w")
        e = date_add(startof(self.now, "w"), 1, "w")
        return s, e


# noinspection PyPep8Naming,NonAsciiCharacters
class DayProcessor(HabitProcessor):
    def __init__(self):
        synonym = {"天": ["日"]}
        super(DayProcessor, self).__init__(synonym)

    def 今天(self):
        s = startof(self.now, "d")
        e = endof(s, "d")
        return s, e

    def 明天(self):
        s = date_add(startof(self.now, "d"), 1, "d")
        e = endof(s, "d")
        return s, e

    def 后天(self):
        s = date_add(startof(self.now, "d"), 2, "d")
        e = endof(s, "d")
        return s, e

    def 昨天(self):
        s = date_sub(startof(self.now, "d"), 1, "d")
        e = endof(s, "d")
        return s, e

    def 前天(self):
        s = date_sub(startof(self.now, "d"), 2, "d")
        e = endof(s, "d")
        return s, e

    def 上午(self):
        s = startof(self.now, "am")
        e = endof(s, "am")
        return s, e

    def 下午(self):
        s = startof(self.now, "pm")
        e = endof(s, "pm")
        return s, e

    def 前几天(self, n: int):
        """
        例如：当前时间 2021/10/1，前三天，即 2021/9/28 - 2021/10/1
        """
        s = date_sub(startof(self.now, "d"), n, "d")
        e = startof(self.now, "d")
        return s, e

    def 后几天(self, n: int):
        """
        例如：当前时间 2021/10/1，后三天，即 2021/10/2 - 2021/10/5
        """
        s = date_add(startof(self.now, "d"), 1, "d")
        e = date_add(s, n, "d")
        return s, e

    def 几天前(self, n: int):
        """
        例如：当前时间 2021/10/1，三天前，即 2021/9/28 - 2021/9/29
        """
        s = date_sub(startof(self.now, "d"), n, "d")
        e = endof(s, "d")
        return s, e

    def 几天后(self, n: int):
        """
        例如：当前时间 2021/10/1，三天后，即 2021/10/4 - 2021/10/5
        """
        s = date_add(startof(self.now, "d"), n, "d")
        e = endof(s, "d")
        return s, e

    def 几天内(self, n: int):
        """
        例如：当前时间 2021/10/1，三天内，即 2021/9/29 - 2021/10/2
        """
        s = date_sub(startof(self.now, "d"), n - 1, "d")
        e = date_add(startof(self.now, "d"), 1, "d")
        return s, e


def create_processor(text: str) -> HabitProcessor:
    processor: Union[HabitProcessor, None] = None

    if "年" in text:
        processor = YearProcessor()
    elif "季度" in text:
        processor = QuarterProcessor()
    elif "月" in text:
        processor = MonthProcessor()
    elif "周" in text or "星期" in text:
        processor = WeekProcessor()
    elif "天" in text or "日" in text or "午" in text:
        processor = DayProcessor()

    return processor
