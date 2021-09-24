import re

from datetime import datetime
from typing import List, Dict, Tuple, Union
from lark import Lark

from .visitors import DateTreeVisitor
from .util import str2digit, build_date, dateformat
from .processors import create_processor


date_grammar = r"""
    start: date
    
    date: years
        | years? months
        | (years? months)? days "当天"?
        | _cn_word
        | years? months? (days "当天"?)? comb_part
    
    _cn_word: "第"? (WORD | WORD WORD)? DIGIT? "个"? UNIT ("份" | "度" | "以" | "之")? WORD?
    
    comb_part: WORD+ UNIT | "第"? DIGIT "个"? UNIT
    
    years : DIGIT DIGIT (DIGIT DIGIT)? ("年" | "-" | "/")
    months: DIGIT DIGIT? ("月" | "月份" | "-" | "/")
    days  : DIGIT (DIGIT DIGIT?)? ("日" | "号")?
    
    WORD : "今" | "本" | "当" | "这个" | "当前" | "明" | "后" | "昨" | "去" | "上" | "下" | "前" | "后" | "内" | "以来" | "半"
    UNIT : "年" | "季度" | "月" | "周" | "星期" | "天" | "日" | "午"
    DIGIT: /["0-9零一二两三四五六七八九十"]/
    
    // Disregard spaces in text
    %ignore " "
"""


class Cn2Date:
    def parse(self, inputs: str) -> Union[Tuple[str, str], None]:
        if inputs is None or inputs.isspace():
            return None

        # 解析语句
        tree = Lark(date_grammar).parse(inputs)
        visitor = DateTreeVisitor()
        visitor.visit(tree)

        if visitor.options is None:
            return None

        # 处理 中文口语
        if type(visitor.options) == str:
            result = self.__parse_cn_word(visitor.options)

        # 处理 年月日格式
        elif type(visitor.options) == dict:
            result = build_date(**visitor.options)

        # 处理 组合日期格式
        else:
            result = self.__parse_comb_date(visitor.options[0], visitor.options[1])

        if result is None:
            return None

        return dateformat(result[0]), dateformat(result[1])

    @staticmethod
    def __parse_cn_word(inputs: str) -> Union[List[datetime], None]:
        processor = create_processor(inputs)
        if processor is None:
            return None

        args = []

        # 处理 参数，例如 前n年、后n年...
        side_words = ["前", "后", "内"]
        if inputs[0] in side_words or inputs[-1] in side_words:
            rq_pattern = re.compile(
                r"^(?P<prefix>[前后])?(?P<digit>[0-9零一二两三四五六七八九十])个?(?:[年月周日天]|星期|季度)以?(?P<suffix>[前后内]|以来)?$")
            result = rq_pattern.search(inputs)
            if result:
                digit_str = result.group("digit")
                inputs = inputs.replace(digit_str, "几")
                args.append(str2digit(digit_str))

        return processor.process(inputs, *tuple(args))

    def __parse_comb_date(self, date_dict: Dict[str, int], comb_str: str) -> Union[List[datetime], None]:
        result = build_date(**date_dict)

        if result is None:
            return None

        result2 = self.__parse_cn_word(comb_str)

        if len(result2) == 0:
            pass

        date_list = []
        for i, dt in enumerate(result):
            rpc_date = result2[i]
            date_list.append(dt.replace(month=rpc_date.month, day=rpc_date.day))

        if result2[0].year == result2[1].year:
            date_list[1] = date_list[1].replace(year=date_list[0].year)

        return date_list
