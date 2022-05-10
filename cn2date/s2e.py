from datetime import datetime
from typing import Tuple


class S2E:
    def __init__(self, start: datetime, end: datetime) -> None:
        self.start = start
        self.end = end

    def to_tuple(self) -> Tuple[datetime, datetime]:
        return self.start, self.end
