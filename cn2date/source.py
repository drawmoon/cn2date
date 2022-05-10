from enum import IntEnum
from typing import Dict, List, Union

from cn2date.s2e import S2E


class Intent(IntEnum):
    Date = 1
    NL = 2
    Group = 3
    

class Source:
    def __init__(self, intent: Intent, terminative: Dict[str, S2E], next: List[str]) -> None:
        self.intent = intent
        self.terminative = terminative
        self.next = next


def last(source: Source) -> Union[S2E, None]:
    if any(source.next):
        return None

    return list(source.terminative.values())[0]
