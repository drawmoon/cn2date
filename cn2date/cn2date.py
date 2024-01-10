from os import path
from typing import Optional

from lark import Lark

from .transform import ChineDateTransformer, DateBetween, NormDateTransformer, transform

__dir__ = path.dirname(__file__)

# 标准日期格式字符解析
NORM_DATE_GRAMMAR_FILE = path.join(__dir__, "norm_date.lark")
# 口语化日期格式字符解析
CHINE_DATE_GRAMMAR_FILE = path.join(__dir__, "chine_date.lark")

_dict = dict()


def parse(s: str) -> Optional[DateBetween]:
    func_arr = [_norm_date_parse, _chine_date_parse]
    for func in func_arr:
        dt = func(s)
        if dt:
            return dt
    return None


def _norm_date_parse(s: str) -> DateBetween:
    if "norm_date" not in _dict:
        _dict["norm_date"] = _l(
            NORM_DATE_GRAMMAR_FILE,
            parser="earley",
            propagate_positions=False,
            maybe_placeholders=False,
        )
    return transform(s, lark=_dict["norm_date"], transformer=NormDateTransformer())


def _chine_date_parse(s: str) -> DateBetween:
    if "chine_date" not in _dict:
        _dict["chine_date"] = _l(
            CHINE_DATE_GRAMMAR_FILE,
            parser="lalr",
            propagate_positions=False,
            maybe_placeholders=False,
        )
    return transform(
        s,
        lark=_dict["chine_date"],
        transformer=ChineDateTransformer(),
    )


def _l(filepath: str, **options) -> Lark:
    with open(filepath, encoding="utf8") as f:
        lark = Lark(
            f,
            **options,
        )
    return lark
