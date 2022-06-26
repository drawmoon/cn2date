from __future__ import annotations

from typing import Callable, Optional

from cn2date.nl.selector import Selector


class SelectorMethod:
    """ """

    name: str = None
    __rule: Callable[[str], bool] | None

    def __init__(self, name: str, rule: Optional[Callable[[str], bool]] = None):
        """ """
        self.name = name
        self.__rule = rule

    def __call__(self, fn):
        fn.__setattr__("__selector__", Selector(self.name, fn, self.__rule))
        return fn
