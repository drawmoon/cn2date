# pyright: strict

from __future__ import annotations

from datetime import datetime


class S2E:
    def __init__(self, start: datetime, end: datetime) -> None:
        self.start = start
        self.end = end

    def to_tuple(self) -> tuple[datetime, datetime]:
        return self.start, self.end
