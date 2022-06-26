# pyright: strict

from __future__ import annotations

from typing import Callable, Optional

from lark import Lark, Tree, UnexpectedCharacters

from cn2date.config import get_default_conf
from cn2date.nl.selector import Selector
from cn2date.nl.year import _YearSelector
from cn2date.transform_info import TransformInfo
from cn2date.util import endof
from cn2date.visitors import DateTreeVisitor, NLTreeVisitor


class TransformerBase:
    """ """

    transform_info: TransformInfo

    def __init__(self, synonym: Optional[dict[str, list[str]]] = None):
        """

        :param synonym: 代名词
        """
        self.synonym = synonym

    def initialize(self, transform_info: TransformInfo) -> TransformerBase:
        """ """
        self.transform_info = transform_info
        self._handle_synonym()
        return self

    def _handle_synonym(self) -> None:
        """
        处理代名词
        """
        text = self.transform_info.input
        if self.synonym is not None:
            for k, synonyms in self.synonym.items():
                for synonym in synonyms:
                    text = text.replace(synonym, k)
        self.transform_info.input = text
        self.transform_info.synonym = self.synonym

    def transform(self) -> bool:
        """ """
        return False


class LarkTransformer(TransformerBase):
    """ """

    def _parse(self, grammar: str) -> Tree | None:
        """ """
        try:
            parser = Lark(grammar)
            return parser.parse(self.transform_info.input)
        except UnexpectedCharacters:  # 传入的字符串匹配 lark 失败
            return None


class DateTransformer(LarkTransformer):
    """ """

    def transform(self) -> bool:
        """ """

        tree = self._parse(get_default_conf()[0])
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
        """ """
        super(NLTransformer, self).initialize(transform_info)
        if not any(self.__selectors):
            self.__add_default_selector()
        return self

    def get_selectors(self) -> list[str]:
        """ """
        return list(self.__selectors.keys())

    def add_selector(self, selector: Selector) -> NLTransformer:
        """ """
        if selector.name in self.__selectors:
            raise ValueError(f"Selectors with the same key already exist: {selector.name}")

        self.__selectors[selector.name] = selector

        return self

    def remove_selector(self, name: str) -> NLTransformer:
        """ """
        if name in self.__selectors:
            self.__selectors.pop(name)
        return self

    def __add_default_selector(self) -> None:
        """ """
        selectors = _YearSelector().selectors
        for selector in selectors:
            self.__selectors[selector.name] = selector

    def transform(self) -> bool:
        """ """
        tree = self._parse(get_default_conf()[1])

        visitor = NLTreeVisitor().initialize(self.transform_info)
        visitor.visit(tree)

        if self.transform_info.current in self.__selectors:
            self.__selectors[self.transform_info.current].eval(self.transform_info)
            if self.transform_info.result is None:
                raise ValueError("No content written to output")
            self.transform_info.intent = "nl"
            return True

        for selector in list(self.__selectors.values()):
            if selector.match(self.transform_info.current):
                if selector.eval(self.transform_info):
                    if self.transform_info.result is None:
                        raise ValueError("No content written to output")
                    self.transform_info.intent = "nl"
                    return True

        return False
