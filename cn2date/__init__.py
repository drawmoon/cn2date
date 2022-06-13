from pathlib import Path
from typing import List

from lark import Lark

from cn2date.transform import DateTransformer

from .cn2date import Cn2Date

__version__ = "0.0.4"


def read_default_conf() -> List[str]:
    file = Path(__file__).parent / "date.lark"
    text = open(file, "r", encoding="utf-8").read()
    return text.split("===")


def create_default_parser() -> Cn2Date:
    confs = read_default_conf()
    return Cn2Date().add_ext(DateTransformer(Lark(confs[0])))


default = create_default_parser()

parse = default.parse
