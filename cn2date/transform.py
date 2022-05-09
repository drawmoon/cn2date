from typing import Dict, List, Optional

from lark import Lark

from cn2date.profiler import Intent
from cn2date.source import Source
from cn2date.visitors import DateTreeVisitor, VisitorBase, value_from, visit


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
    def __init__(self, parser: Lark):
        super(DateTransformer, self).__init__(parser, DateTreeVisitor())

    def transform(self, text: str) -> Source:
        ctx = visit(self._visitor, self._parser, text)

        s2e = value_from(ctx)

        return Source(Intent.Date, {ctx.mark: s2e}, ctx.ignore)
