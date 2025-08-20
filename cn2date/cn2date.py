from os import path
from typing import Optional

from lark import Lark

from .exception import DateParseException
from .transform import ChineDateTransformer, DateBetween, NormDateTransformer

__dir__ = path.dirname(__file__)

# 标准日期格式字符解析
NORM_DATE_GRAMMAR_FILE = path.join(__dir__, "norm_date.lark")
# 口语化日期格式字符解析
CHINE_DATE_GRAMMAR_FILE = path.join(__dir__, "chine_date.lark")

_dict = dict()


def parse(text: str) -> Optional[DateBetween]:
    date_object = parse_norm_date(text)
    if not date_object:
        return parse_chine_date(text)
    return None


def parse_norm_date(s: str) -> DateBetween:
    if "norm_date" not in _dict:
        _dict["norm_date"] = _make_lark_parser(
            NORM_DATE_GRAMMAR_FILE,
            parser="earley",
            propagate_positions=False,
            maybe_placeholders=False,
        )
    try:
        transformer = NormDateTransformer()
        return transformer.invoke(s, lark=_dict["norm_date"])
    except DateParseException:
        return None


def parse_chine_date(s: str) -> DateBetween:
    if "chine_date" not in _dict:
        _dict["chine_date"] = _make_lark_parser(
            CHINE_DATE_GRAMMAR_FILE,
            parser="lalr",
            propagate_positions=False,
            maybe_placeholders=False,
        )
    try:
        transformer = ChineDateTransformer()
        return transformer.invoke(s, lark=_dict["chine_date"])
    except DateParseException:
        return None


def _make_lark_parser(filepath: str, **options) -> Lark:
    with open(filepath, encoding="utf8") as f:
        lark = Lark(
            f,
            **options,
        )
    return lark
