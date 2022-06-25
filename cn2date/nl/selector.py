from __future__ import annotations

import inspect
from typing import Callable

from cn2date.transform_info import TransformInfo


class SelectorBase:
    """ """

    items: dict[str, Callable[[TransformInfo], bool]] = {}

    def __init__(self):
        """ """
        # 自动注册标记 @SelectorMethod 装饰器的方法
        fn_list = inspect.getmembers(self, inspect.ismethod)
        for (n, m) in fn_list:
            if "__tag__" in m.__dict__:
                self.__expose(m.__dict__["__tag__"], m)

    def __expose(self, name: str, fn: Callable[[TransformInfo], bool]) -> None:
        """ """
        if name in self.items:
            raise ValueError(f"Same key already exist: {name}")
        self.items[name] = fn
