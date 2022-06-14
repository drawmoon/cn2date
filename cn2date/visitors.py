from typing import List

from lark import Token, Tree, Visitor
from typing_extensions import Self

from cn2date.util import DateBuilder, date_part, now


class VisitorContext:
    def __init__(self) -> None:
        self.depth: str = "y"
        self.bldr = DateBuilder()
        self.mark = ""
        self.ignore: List[str] = []


class VisitorBase(Visitor):
    ctx: VisitorContext

    def initialize(self) -> Self:
        self.ctx = VisitorContext()
        return self

    def _get_node_value(self, node: Tree) -> str:
        if node is None:
            raise ValueError("The current node is None")

        children = node.children

        if not all(isinstance(c, Token) for c in children):
            raise TypeError("The child of tree is not Token")

        return "".join([c.value for c in children])


class DateTreeVisitor(VisitorBase):
    def years(self, tree: Tree) -> None:
        val = self._get_node_value(tree)
        year_part = date_part(val, "y")

        self.ctx.bldr.year(year_part)
        self.ctx.depth = "y"

    def months(self, tree: Tree) -> None:
        val = self._get_node_value(tree)
        month_part = date_part(val)

        self.ctx.bldr.month(month_part)
        self.ctx.depth = "y.m"

    def days(self, tree: Tree) -> None:
        if self.ctx.depth != "y.m":
            self.ctx.bldr.month(now().month)

        val = self._get_node_value(tree)
        day_part = date_part(val)

        self.ctx.bldr.day(day_part)
        self.ctx.depth = "y.m.d"
