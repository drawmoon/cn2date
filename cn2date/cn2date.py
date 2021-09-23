import re

from datetime import datetime
from typing import List, Tuple, Union
from lark import Lark

from .visitors import DateTreeVisitor
from .util import str2digit, build_date, dateformat
from .processors import create_processor


date_grammar = r"""
    start: date | cn_word
    
    date   : ((years? months)? days) "当天"? | years? months? | (years | months) comb
    cn_word: "第"? (WORD | WORD WORD)? DIGIT? "个"? UNIT ("份" | "度" | "以" | "之")? WORD?
    
    years : DIGIT DIGIT (DIGIT DIGIT)? ("年" | "-" | "/")
    months: DIGIT DIGIT? ("月" | "月份" | "-" | "/")
    days  : DIGIT (DIGIT DIGIT?)? ("日" | "号")?
    comb  : COMD | "第"? DIGIT "个"? UNIT
    
    COMD : "上半年" | "下半年"
    WORD : "今" | "本" | "这个" | "当前" | "明" | "后" | "昨" | "上" | "下" | "前" | "后" | "内" | "以来" | "去" | "半"
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

        # 处理 中文口语
        if visitor.cn_word_part is not None:
            result = self.__parse_cn_word(visitor.cn_word_part)
            return dateformat(result[0]), dateformat(result[1])

        # 处理 年月日格式 的字符
        params = {}
        for key, val in visitor.date_dict.items():
            digit = str2digit(val, key)
            if digit is not None:
                params[key] = digit
        result = build_date(**params)
        if visitor.comb_part is not None:
            result = self.__parse_comb_date(result, visitor.comb_part)
        return None if len(result) == 0 else dateformat(result[0]), dateformat(result[1])

    @staticmethod
    def __parse_cn_word(inputs: str) -> List[datetime]:
        processor = create_processor(inputs)
        if processor is None:
            return []

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

    def __parse_comb_date(self, date_lst: List[datetime], comb_str: str) -> List[datetime]:
        result = self.__parse_cn_word(comb_str)
        if len(result) == 0:
            pass
        date_list = []
        for i, dt in enumerate(date_lst):
            rpc_date = result[i]
            date_list.append(dt.replace(month=rpc_date.month, day=rpc_date.day))
        if result[0].year == result[1].year:
            date_list[1] = date_list[1].replace(year=date_list[0].year)
        return date_list
