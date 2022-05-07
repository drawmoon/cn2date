from typing import Dict, List, Optional

from lark import Lark

from cn2date.source import Source
from cn2date.visitors import VisitorBase, value_from


class TransformerBase:
    def __init__(
        self,
        parser: Lark,
        visitor: VisitorBase,
        synonym: Optional[Dict[str, List[str]]] = None,
    ):
        self._parser = parser
        self._visitor = visitor
        self._synonym = synonym

    def transform(self, text: str) -> Source:
        pass


class DateTransformer(TransformerBase):
    def __init__(self, parser: Lark, visitor: VisitorBase):
        super(DateTransformer, self).__init__(parser, visitor)

    def transform(self, text: str) -> Source:
        t = self._parser.parse(text)
        self._visitor.visit(t)

        s2e = value_from(self._visitor.get_context())
