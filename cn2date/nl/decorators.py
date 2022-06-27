from __future__ import annotations

from typing import Callable, Optional

from cn2date.nl.selector import Selector


class SelectorMethod:
    """ """

    name: str = None
    __rule: Callable[[str], bool] | None
    synonym: dict[str, list[str]] | None

    def __init__(
        self, name: str, rule: Optional[Callable[[str], bool]] = None, synonym: Optional[dict[str, list[str]]] = None
    ):
        """

        :param name:
        :param rule:
        :param synonym:
        """
        self.name = name
        self.__rule = rule
        self.synonym = synonym

    def __call__(self, fn):
        selector = Selector(self.name, fn, self.__rule, self.synonym)
        fn.__setattr__("__selector__", selector)
        return fn
