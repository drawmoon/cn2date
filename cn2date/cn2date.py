from datetime import datetime
from typing import Tuple

from cn2date.profiler import Intent, Profiler, preceded


class Cn2Date:
    def __init__(self) -> None:
        self.profiler = Profiler()

    def parse(self, text: str) -> Tuple[datetime, datetime]:
        if text is None or text.isspace():
            raise ValueError("The parameter text is None or empty")

        return preceded(
            (
                self.profiler.get_transformer(Intent.Date),
                self.profiler.get_transformer(Intent.NL),
            ),
            text,
        ).to_tuple()
