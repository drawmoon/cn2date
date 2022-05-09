from pathlib import Path
from typing import Dict, Tuple

from lark import Lark

from cn2date.s2e import S2E
from cn2date.source import Intent, last
from cn2date.transform import DateTransformer, TransformerBase


class Profiler:
    __xfmr_dict: Dict[Intent, TransformerBase] = {}

    def __init__(self) -> None:
        g_dict = self.__read_conf()

        self.__xfmr_dict[Intent.Date] = DateTransformer(Lark(g_dict[Intent.Date]))

    def __read_conf(self) -> Dict[Intent, str]:
        intent_list = [intent for intent in Intent]

        file = Path(__file__).parent / "date.lark"
        text = open(file, "r", encoding="utf-8").read()

        return dict(zip(intent_list, text.split("===")))

    def get_transformer(self, intent: Intent) -> TransformerBase:
        return self.__xfmr_dict[intent]


def preceded(t: Tuple[TransformerBase], text: str) -> S2E:
    for xfmr in t:
        source = xfmr.transform(text)

        s2e = last(source)

        if s2e is not None:
            return s2e

    pass
