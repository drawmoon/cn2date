# pyright: strict

from __future__ import annotations

from typing import Any, Callable, Optional, TypeVar

from cn2date.nl.selector import Selector

TFunc = TypeVar("TFunc", bound=Callable[..., Any])


class SelectorMethod:
    """ """

    name: str
    __rule: Callable[[str], bool] | None
    synonym: dict[str, list[str]] | None

    def __init__(
        self, name: str, rule: Optional[Callable[[str], bool]] = None, synonym: Optional[dict[str, list[str]]] = None
    ) -> None:
        """

        :param name:
        :param rule:
        :param synonym:
        """
        self.name = name
        self.__rule = rule
        self.synonym = synonym

    def __call__(self, fn: TFunc) -> TFunc:
        selector = Selector(self.name, fn, self.__rule, self.synonym)
        fn.__setattr__("__selector__", selector)
        return fn
