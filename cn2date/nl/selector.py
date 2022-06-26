from __future__ import annotations

import inspect
from typing import Callable, Optional

from cn2date.transform_info import TransformInfo


class Selector:
    """ """

    name: str
    __fn: Callable[[TransformInfo], bool]
    __rule: Callable[[str], bool]

    def __init__(
        self, name: str, fn: Callable[[TransformInfo], bool], rule: Optional[Callable[[str], bool]] = None
    ) -> None:
        """

        :param name:
        :param fn:
        :param rule:
        """
        self.name = name
        self.__fn = fn
        self.__rule = rule

    def match(self, text: str) -> bool:
        """ """
        return self.__rule(text) if self.__rule is not None else text == self.name

    def eval(self, transform_info: TransformInfo) -> bool:
        """ """
        return self.__fn(transform_info)


class SelectorBase:
    """ """

    selectors: list[Selector] = []

    def __init__(self):
        """ """
        # 自动注册标记 @SelectorMethod 装饰器的方法
        fn_list = inspect.getmembers(self, inspect.isfunction)
        for (_, m) in fn_list:
            if "__selector__" in m.__dict__:
                self.__safe_add(m.__dict__["__selector__"])

    def __safe_add(self, selector: Selector) -> None:
        """ """
        if selector.name in [s.name for s in self.selectors]:
            raise ValueError(f"Same key already exist: {selector.name}")
        self.selectors.append(selector)
