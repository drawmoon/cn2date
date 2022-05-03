from typing import Dict, List, Optional

from lark import Lark, Visitor

from cn2date.source import Source


class TransformerBase:
    def __init__(
        self,
        parser: Lark,
        visitor: Visitor,
        synonym: Optional[Dict[str, List[str]]] = None,
    ):
        self._parser = parser
        self._visitor = visitor
        self._synonym = synonym

    def transform(self) -> Source:
        pass


class DateTransformer(TransformerBase):
    def __init__(self, parser: Lark, visitor: Visitor):
        super(DateTransformer, self).__init__(parser, visitor)

    def transform(self) -> Source:
        pass
