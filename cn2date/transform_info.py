from __future__ import annotations

from datetime import datetime

from typing_extensions import Literal

from cn2date.s2e import S2E


class TransformInfo:
    base_str: str
    synonym: dict[str, list[str]] | None
    current: str | None
    result: S2E | None
    intent: Literal["date", "nl", "group"] | str | None

    def initialize(self, base_str: str) -> TransformInfo:
        self.base_str = base_str
        self.synonym = None
        self.current = None
        self.result = None
        self.intent = None

        return self

    def write(self, start: datetime, end: datetime) -> None:
        self.result = S2E(start, end)
        self.current = None
