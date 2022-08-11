# pyright: strict

from __future__ import annotations

from lark import Lark, Tree, UnexpectedCharacters

from cn2date.nl.day import DaySelectorSet
from cn2date.nl.month import MonthSelectorSet
from cn2date.nl.quarter import QuarterSelectorSet
from cn2date.nl.selector import Selector
from cn2date.nl.week import WeekSelectorSet
from cn2date.nl.year import YearSelectorSet
from cn2date.transform_info import TransformInfo
from cn2date.util import endof, get_settings
from cn2date.visitors import DateTreeVisitor, NLTreeVisitor


class TransformerBase:
    """ """

    transform_info: TransformInfo

    def initialize(self, transform_info: TransformInfo) -> TransformerBase:
        """

        :param transform_info:
        :return:
        """
        self.transform_info = transform_info
        return self

    def transform(self) -> bool:
        """

        :return:
        """
        return False


class LarkTransformer(TransformerBase):
    """ """

    _settings = get_settings()

    def _parse(self, grammar: str) -> Tree | None:
        """

        :param grammar:
        :return:
        """
        try:
            parser = Lark(grammar)
            return parser.parse(self.transform_info.input)
        except UnexpectedCharacters:  # 传入的字符串匹配 lark 失败
            return None


class DateTransformer(LarkTransformer):
    """ """

    def transform(self) -> bool:
        """

        :return:
        """

        tree = self._parse(self._settings["date_lark_grammar"])
        if tree is None:
            return False

        visitor = DateTreeVisitor().initialize(self.transform_info)
        visitor.visit(tree)

        start = visitor.builder.build()
        if visitor.depth == 0:
            self.transform_info.write(start, endof(start, "y"))
        elif visitor.depth == 1:
            self.transform_info.write(start, endof(start, "m"))
        else:
            self.transform_info.write(start, endof(start, "d"))

        self.transform_info.intent = "date"

        return True


class NLTransformer(LarkTransformer):
    """ """

    __selectors: dict[str, Selector] = {}

    def initialize(self, transform_info: TransformInfo) -> NLTransformer:
        """

        :param transform_info:
        :return:
        """
        super(NLTransformer, self).initialize(transform_info)
        if not any(self.__selectors):
            self.__add_default_selector()
        return self

    def get_selectors(self) -> list[str]:
        """

        :return:
        """
        return list(self.__selectors.keys())

    def add_selector(self, selector: Selector) -> NLTransformer:
        """

        :param selector:
        :return:
        """
        if selector.name in self.__selectors:
            raise ValueError(f"Selectors with the same key already exist: {selector.name}")

        self.__selectors[selector.name] = selector

        return self

    def remove_selector(self, name: str) -> NLTransformer:
        """

        :param name:
        :return:
        """
        if name in self.__selectors:
            self.__selectors.pop(name)
        return self

    def __add_default_selector(self) -> None:
        """ """
        selectors = [
            *YearSelectorSet().items,
            *QuarterSelectorSet().items,
            *MonthSelectorSet().items,
            *WeekSelectorSet().items,
            *DaySelectorSet().items,
        ]
        for selector in selectors:
            self.add_selector(selector)

    def transform(self) -> bool:
        """

        :return:
        """
        tree = self._parse(self._settings["nl_lark_grammar"])
        if tree is None:
            return False

        visitor = NLTreeVisitor().initialize(self.transform_info)
        visitor.visit(tree)

        if self.transform_info.current in self.__selectors:
            self.__selectors[self.transform_info.current].eval(self.transform_info)
            if self.transform_info.result is None:
                raise ValueError("No content written to output")
            self.transform_info.intent = "nl"
            return True

        for selector in list(self.__selectors.values()):
            if selector.eval(self.transform_info):
                if self.transform_info.result is None:
                    raise ValueError("No content written to output")
                self.transform_info.intent = "nl"
                return True

        return False
