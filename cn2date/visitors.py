# pyright: strict

from __future__ import annotations

from typing import Any

from lark import Token, Tree, Visitor

from cn2date.transform_info import TransformInfo
from cn2date.util import DateBuilder, date_part, none_or_whitespace, now


class VisitorBase(Visitor[Any]):
    """ """

    transform_info: TransformInfo

    def initialize(self, transform_info: TransformInfo) -> VisitorBase:
        """

        :param transform_info:
        :return:
        """
        self.transform_info = transform_info
        return self

    def _take(self, node: Tree) -> None:
        """

        :param node:
        :return:
        """
        if node is None:
            raise ValueError("The current node is None")

        # 更换节点后必须重新设置当前值为初始值
        self.transform_info.current = ""

        for child in node.children:
            if not isinstance(child, Token):
                raise TypeError("The child of tree is not Token")
            self.transform_info.current += child

        if none_or_whitespace(self.transform_info.current):
            raise ValueError("Failed to take value of the current node")


class DateTreeVisitor(VisitorBase):
    """ """

    builder: DateBuilder
    depth: int

    def initialize(self, transform_info: TransformInfo) -> DateTreeVisitor:
        """

        :param transform_info:
        :return:
        """
        super(DateTreeVisitor, self).initialize(transform_info)
        self.builder = DateBuilder()
        self.depth = 0
        return self

    def years(self, tree: Tree) -> None:
        """

        :param tree:
        :return:
        """
        self._take(tree)
        year = date_part(self.transform_info.current, "y")
        self.builder.year(year)
        self.depth = 0

    def months(self, tree: Tree) -> None:
        """

        :param tree:
        :return:
        """
        self._take(tree)
        month = date_part(self.transform_info.current)
        self.builder.month(month)
        self.depth = 1

    def days(self, tree: Tree) -> None:
        """

        :param tree:
        :return:
        """
        self._take(tree)
        day = date_part(self.transform_info.current)
        self.builder.day(day)
        if self.depth < 1:
            self.builder.month(now().month)
        self.depth = 2


class NLTreeVisitor(VisitorBase):
    """ """

    def nl(self, tree: Tree) -> None:
        """

        :param tree:
        :return:
        """
        self._take(tree)
