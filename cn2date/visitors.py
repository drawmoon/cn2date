from __future__ import annotations

from lark import Token, Tree, Visitor

from cn2date.transform_info import TransformInfo
from cn2date.util import DateBuilder, date_part, now


class VisitorBase(Visitor):
    def __init__(self) -> None:
        self.transform_info: TransformInfo | None = None

    def initialize(self, transform_info: TransformInfo) -> VisitorBase:
        self.transform_info = transform_info
        return self

    def _take(self, node: Tree) -> None:
        if node is None:
            raise ValueError("The current node is None")

        self.transform_info.current = ""

        for child in node.children:
            if not isinstance(child, Token):
                raise TypeError("The child of tree is not Token")
            self.transform_info.current += child


class DateTreeVisitor(VisitorBase):
    builder: DateBuilder
    depth: int

    def initialize(self, transform_info: TransformInfo) -> DateTreeVisitor:
        super(DateTreeVisitor, self).initialize(transform_info)
        self.builder = DateBuilder()
        self.depth = 0
        return self

    def years(self, tree: Tree) -> None:
        self._take(tree)
        year = date_part(self.transform_info.current, "y")
        self.builder.year(year)
        self.depth = 0

    def months(self, tree: Tree) -> None:
        self._take(tree)
        month = date_part(self.transform_info.current)
        self.builder.month(month)
        self.depth = 1

    def days(self, tree: Tree) -> None:
        if self.depth < 1:
            self.builder.month(now().month)

        self._take(tree)
        day = date_part(self.transform_info.current)
        self.builder.day(day)
        self.depth = 2
