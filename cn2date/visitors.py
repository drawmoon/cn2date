from lark import Visitor, Tree, Token
from typing import Dict, Union

from cn2date.util import now


class DateTreeVisitor(Visitor):
    date_dict: Dict[str, str]
    comb_part: Union[str, None]
    cn_word_part: Union[str, None]

    def __init__(self):
        self.date_dict = {}
        self.comb_part = None
        self.cn_word_part = None

    def years(self, tree: Tree) -> None:
        self.date_dict["year"] = self.__scan_values(tree)

    def months(self, tree: Tree) -> None:
        today = now()
        keys = self.date_dict.keys()
        if "year" not in keys:
            self.date_dict["year"] = str(today.year)
        self.date_dict["month"] = self.__scan_values(tree)

    def days(self, tree: Tree) -> None:
        today = now()
        keys = self.date_dict.keys()
        if "year" not in keys:
            self.date_dict["year"] = str(today.year)
        if "month" not in keys:
            self.date_dict["month"] = str(today.month).rjust(2, "0")
        self.date_dict["day"] = self.__scan_values(tree)

    def comb(self, tree: Tree) -> None:
        self.comb_part = self.__scan_values(tree)

    def cn_word(self, tree: Tree) -> None:
        self.cn_word_part = self.__scan_values(tree)

    @staticmethod
    def __scan_values(tree: Tree) -> str:
        val = ""
        for child in tree.children:
            if not isinstance(child, Token):
                raise TypeError("子节点不是 Token")
            val += child.value
        return val
