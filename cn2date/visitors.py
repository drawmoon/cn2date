from typing import List, Literal, Union

from lark import Lark, Token, Tree, Visitor

from cn2date.s2e import S2E
from cn2date.util import DateBuilder, endof, date_part, now


class VisitorContext:
    def __init__(self):
        self.depth: str = "y"
        self.bldr = DateBuilder()
        self.mark = ""
        self.ignore: List[str] = []


class VisitorBase(Visitor):
    _ctx: VisitorContext

    def prepare(self):
        self._ctx = VisitorContext()

    def _get_node_value(self, node: Tree) -> str:
        if node is None:
            raise ValueError("The current node is None")

        children = node.children

        if not all(isinstance(c, Token) for c in children):
            raise TypeError("The child of tree is not Token")

        return "".join([c.value for c in children])

    def get_context(self) -> VisitorContext:
        return self._ctx


class DateTreeVisitor(VisitorBase):
    def years(self, tree: Tree) -> None:
        val = self._get_node_value(tree)
        year_part = date_part(val, "y")

        self._ctx.bldr.year(year_part)
        self._ctx.depth = "y"

    def months(self, tree: Tree) -> None:
        val = self._get_node_value(tree)
        month_part = date_part(val)

        self._ctx.bldr.month(month_part)
        self._ctx.depth = "y.m"

    def days(self, tree: Tree) -> None:
        if self._ctx.depth != "y.m":
            self._ctx.bldr.month(now().month)

        val = self._get_node_value(tree)
        day_part = date_part(val)

        self._ctx.bldr.day(day_part)
        self._ctx.depth = "y.m.d"


def visit(v: VisitorBase, parser: Lark, text: str, threshold=3) -> VisitorContext:
    if threshold <= 0:
        ctx = VisitorContext()
        ctx.ignore = [text]
        return ctx

    try:
        tree = parser.parse(text)

        v.prepare()
        v.visit(tree)

        return v.get_context()
    except:
        threshold -= 1

        ignore = text[-1:]
        text = text[:-1]

        ctx = visit(v, parser, text, threshold)
        ctx.mark = text
        ctx.ignore.insert(0, ignore)
        return ctx


def value_from(ctx: VisitorContext) -> S2E:
    start = ctx.bldr.build()

    end = endof(
        start,
        "y" if ctx.depth == "y" else "m" if ctx.depth == "y.m" else "d",
    )

    return S2E(start, end)
