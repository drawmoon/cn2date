from lark import Visitor, Tree, Token
from typing import Dict, Tuple, Union

from cn2date.util import now, str2digit


DateCompose = Tuple[Dict[str, int], str]
Date = Union[Dict[str, int], DateCompose, str]
VisitorOptions = Union[Date, None]


class DateTreeVisitor(Visitor):
    options: VisitorOptions

    def __init__(self):
        self.options = {}

    def date(self, tree: Tree) -> None:
        if len(self.options) == 0:
            self.options = self.__scan_value(tree)

    def years(self, tree: Tree) -> None:
        self.options["year"] = str2digit(self.__scan_value(tree), "year")

    def months(self, tree: Tree) -> None:
        today = now()
        keys = self.options.keys()

        if "year" not in keys:
            self.options["year"] = today.year

        self.options["month"] = str2digit(self.__scan_value(tree))

    def days(self, tree: Tree) -> None:
        today = now()
        keys = self.options.keys()

        if "year" not in keys:
            self.options["year"] = today.year

        if "month" not in keys:
            self.options["month"] = today.month

        self.options["day"] = str2digit(self.__scan_value(tree))

    def comb_part(self, tree: Tree) -> None:
        self.options = (self.options, self.__scan_value(tree))

    @staticmethod
    def __scan_value(tree: Tree) -> str:
        val = ""
        for child in tree.children:
            if not isinstance(child, Token):
                raise TypeError("子节点不是 Token")
            val += child.value
        return val
