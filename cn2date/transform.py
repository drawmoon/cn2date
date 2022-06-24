# pyright: strict

from __future__ import annotations

from typing import Optional

from lark import Lark

from cn2date.config import get_default_conf
from cn2date.transform_info import TransformInfo
from cn2date.util import endof
from cn2date.visitors import DateTreeVisitor


class TransformerBase:
    transform_info: TransformInfo

    def __init__(self, synonym: Optional[dict[str, list[str]]] = None):
        self.synonym = synonym

    def initialize(self, transform_info: TransformInfo) -> TransformerBase:
        self.transform_info = transform_info
        self.transform_info.synonym = self.synonym
        return self

    def transform(self) -> bool:
        return False


class DateTransformer(TransformerBase):
    def transform(self) -> bool:
        parser = Lark(get_default_conf()[0])
        tree = parser.parse(self.transform_info.base_str)

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
