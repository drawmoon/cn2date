import re

from pathlib import Path
from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import List, Tuple, Union
from lark import Lark

from .visitors import DateTreeVisitor, DateGroup
from .util import str2digit, build_date, date_format, now
from .processors import create_processor


class Cn2Date:
    def __init__(self):
        self.__lark_parser = Lark.open(str(Path(__file__).parent / "date.lark"))

    def parse(self, inputs: str) -> Union[Tuple[str, str], None]:
        if inputs is None or inputs.isspace():
            return None

        # 解析语句
        tree = self.__lark_parser.parse(inputs)
        visitor = DateTreeVisitor()
        visitor.visit(tree)

        # 处理 年月日格式
        if type(visitor.options) == dict:
            result = build_date(**visitor.options)

        # 处理 中文口语
        elif type(visitor.options) == str:
            result = self.__parse_spoken_lang(visitor.options)

        # 处理 组合日期格式
        else:
            result = self.__parse_date_group(visitor.options)

        return None if result is None else date_format(result[0]), date_format(result[1])

    @staticmethod
    def __parse_spoken_lang(inputs: str) -> Union[List[datetime], None]:
        processor = create_processor(inputs)
        if processor is None:
            return None

        # 处理 参数，例如 前n年、后n年...
        args = []
        rq_pattern = re.compile(
            r"^(?P<prefix>[前后])?(?P<digit>[0-9零一二两三四五六七八九十]+)个?(?:[年月周日天]|星期|季度)(?P<suffix>[以之]?[前后内来])?$")
        result = rq_pattern.search(inputs)
        if result and (result.group("prefix") or result.group("suffix")):
            digit_str = result.group("digit")
            inputs = inputs.replace(digit_str, "几")
            args.append(str2digit(digit_str))

        return processor.process(inputs, *tuple(args))

    def __parse_date_group(self, group: DateGroup) -> Union[List[datetime], None]:
        (left, right) = group

        left_date = build_date(**left) if type(left) == dict else self.__parse_spoken_lang(left)
        if left_date is None:
            return None

        if right in ["以前", "之前"]:
            return [datetime.min, left_date[0]]

        if right in ["以后", "之后"]:
            return [left_date[0] + relativedelta(years=1), datetime.max]

        if right == "以来":
            next_day = now() + relativedelta(days=1)
            return [left_date[0], datetime(next_day.year, next_day.month, next_day.day)]

        right_date = self.__parse_spoken_lang(right)
        if right_date is None:
            return left_date

        result: List[datetime] = []
        for i, dt in enumerate(left_date):
            rd = right_date[i]
            result.append(dt.replace(month=rd.month, day=rd.day))

        if right_date[0].year == right_date[1].year:
            result[1] = result[1].replace(year=result[0].year)

        return result
