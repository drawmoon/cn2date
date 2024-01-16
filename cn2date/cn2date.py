from os import path
from typing import Optional

import hanlp
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
    current = transform(
        s,
        lark=_dict["chine_date"],
        transformer=ChineDateTransformer(),
    )
    if current is None:
        dic = _h(s, ["ner/msra", "ner/ontonotes"])
        for _, doc in dic.items():
            for text, typ, _, _ in doc:
                if typ != "DATE":
                    continue
                current = transform(
                    text,
                    lark=_dict["chine_date"],
                    transformer=ChineDateTransformer(),
                    dt=current,
                )
            if current is not None:
                break
    return current


def _l(filepath: str, **options) -> Lark:
    with open(filepath, encoding="utf8") as f:
        lark = Lark(
            f,
            **options,
        )
    return lark


def _h(s: str, m=None, n: str = "default"):
    if n not in _dict:
        _dict[n] = hanlp.load(
            hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH
        )
    handoc = _dict[n](s)
    if m is not None:
        handoc = {k: handoc[k] for k in m}
    return handoc
