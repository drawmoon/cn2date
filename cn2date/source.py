from datetime import datetime
from typing import Tuple, Union

from cn2date.s2e import S2E


class Source:
    def __init__(self) -> None:
        self.intent = ""
        self.terminative = []
        self.next = []


def last(source: Source) -> Union[S2E, None]:
    if not any(source.next):
        pass

    pass
