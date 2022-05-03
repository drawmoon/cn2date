from typing import Literal

from lark import Token, Tree, Visitor

from cn2date.s2e import S2E
from cn2date.util import DateBuilder, endof, now, to_datepart


class VisitorContext:
    type: Literal["2year", "2month", "2day"] = "2year"
    bldr = DateBuilder()


class VisitorBase(Visitor):
    def __init__(self):
        self.ctx = VisitorContext()

    def get_context(self) -> VisitorContext:
        return self.ctx


class DateTreeVisitor(VisitorBase):
    def years(self, tree: Tree) -> None:
        self.ctx.type = "2year"
        self.ctx.bldr.year(to_datepart(scan_value(tree), "year"))

    def months(self, tree: Tree) -> None:
        self.ctx.type = "2month"
        self.ctx.bldr.month(to_datepart(scan_value(tree)))

    def days(self, tree: Tree) -> None:
        self.ctx.type = "2day"
        self.ctx.bldr.day(to_datepart(scan_value(tree)))


def scan_value(tree: Tree) -> str:
    children = tree.children

    if not all(isinstance(c, Token) for c in children):
        raise TypeError("The child of tree is not Token")

    return "".join([c.value for c in children])


def value_from(ctx: VisitorContext) -> S2E:
    start = ctx.bldr.build()

    end = endof(
        start,
        "year" if ctx.type == "2year" else "month" if ctx.type == "2month" else "day",
    )

    return S2E(start, end)
