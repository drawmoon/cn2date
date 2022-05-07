from typing import Literal

from lark import Token, Tree, Visitor

from cn2date.s2e import S2E
from cn2date.util import DateBuilder, endof, to_datepart


class VisitorContext:
    type: Literal["2year", "2month", "2day"] = "2year"
    bldr = DateBuilder()


class VisitorBase(Visitor):
    def __init__(self):
        self._ctx = VisitorContext()

    def get_node_value(tree: Tree) -> str:
        children = tree.children

        if not all(isinstance(c, Token) for c in children):
            raise TypeError("The child of tree is not Token")

        return "".join([c.value for c in children])

    def get_context(self) -> VisitorContext:
        return self._ctx


class DateTreeVisitor(VisitorBase):
    def years(self, tree: Tree) -> None:
        self._ctx.type = "2year"
        self._ctx.bldr.year(to_datepart(self.get_node_value(tree), "year"))

    def months(self, tree: Tree) -> None:
        self._ctx.type = "2month"
        self._ctx.bldr.month(to_datepart(self.get_node_value(tree)))

    def days(self, tree: Tree) -> None:
        self._ctx.type = "2day"
        self._ctx.bldr.day(to_datepart(self.get_node_value(tree)))


def value_from(ctx: VisitorContext) -> S2E:
    start = ctx.bldr.build()

    end = endof(
        start,
        "year" if ctx.type == "2year" else "month" if ctx.type == "2month" else "day",
    )

    return S2E(start, end)
