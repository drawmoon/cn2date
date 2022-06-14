from typing import Dict, List, Optional

from lark import Lark
from typing_extensions import Self

from cn2date.s2e import S2E
from cn2date.source import Intent, Source
from cn2date.util import endof
from cn2date.visitors import DateTreeVisitor


class TransformerContext:
    def __init__(
        self,
        expr: str,
        synonym: Optional[Dict[str, List[str]]] = None,
    ) -> None:
        self.expr = expr
        self.synonym = synonym
        self.current_val: str = None
        self.res = None
        self.exception = None


class ITransformer:
    def __init__(
        self, expr: str, synonym: Optional[Dict[str, List[str]]] = None
    ) -> None:
        self.ctx = TransformerContext(expr, synonym)

    def initialize(self, text: str) -> Self:
        self.ctx.current_val = text
        self.ctx.res = None
        self.ctx.exception = None
        return self

    def transform(self) -> Source:
        pass


class DateTransformer(ITransformer):
    def transform(self) -> Source:
        parser = Lark(self.ctx.expr)
        tree = parser.parse(self.ctx.current_val)

        visitor = DateTreeVisitor().initialize()
        visitor.visit(tree)
        visitor_ctx = visitor.ctx

        start = visitor_ctx.bldr.build()
        end = endof(
            start,
            "y"
            if visitor_ctx.depth == "y"
            else "m"
            if visitor_ctx.depth == "y.m"
            else "d",
        )
        s2e = S2E(start, end)
        return Source(Intent.Date, {visitor_ctx.mark: s2e}, visitor_ctx.ignore)
