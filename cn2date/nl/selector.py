# pyright: strict

from __future__ import annotations

import inspect
from typing import Callable, Optional

from cn2date.transform_info import TransformInfo


class Selector:
    """ """

    name: str
    __fn: Callable[[TransformInfo], bool]
    __rule: Callable[[str], bool] | None
    synonym: dict[str, list[str]] = {"本": ["当前", "这个"], "内": ["以内", "之内"], "以前": ["之前"]}

    def __init__(
        self,
        name: str,
        fn: Callable[[TransformInfo], bool],
        rule: Optional[Callable[[str], bool]] = None,
        synonym: Optional[dict[str, list[str]]] = None,
    ) -> None:
        """

        :param name:
        :param fn:
        :param rule:
        :param synonym:
        """
        self.name = name
        self.__fn = fn
        self.__rule = rule
        if synonym is not None:
            self.synonym = dict(self.synonym, **synonym)

    def __handle_synonym(self, transform_info: TransformInfo) -> None:
        """
        处理代名词
        """
        if self.synonym is None:
            return

        for k, arr in self.synonym.items():
            for s in arr:
                transform_info.current = transform_info.current.replace(s, k)

    def __match(self, transform_info: TransformInfo) -> bool:
        """

        :param transform_info:
        :return:
        """
        return self.__rule(transform_info.current) if self.__rule is not None else transform_info.current == self.name

    def eval(self, transform_info: TransformInfo) -> bool:
        """

        :param transform_info:
        :return:
        """
        self.__handle_synonym(transform_info)
        if not self.__match(transform_info):
            transform_info.current = transform_info.input
            return False
        return self.__fn(transform_info)


class SelectorBase:
    """ """

    selectors: list[Selector] = []
    _synonym: dict[str, list[str]] | None = None

    def __init__(self):
        """ """
        # 自动注册标记 @SelectorMethod 装饰器的方法
        fn_list = inspect.getmembers(self, inspect.isfunction)
        for (_, m) in fn_list:
            if "__selector__" in m.__dict__:
                self.__safe_add(m.__dict__["__selector__"])

    def __safe_add(self, selector: Selector) -> None:
        """

        :param selector:
        :return:
        """
        if selector.name in [s.name for s in self.selectors]:
            raise ValueError(f"Same key already exist: {selector.name}")
        if self._synonym is not None:
            selector.synonym = dict(selector.synonym, **self._synonym)
        self.selectors.append(selector)
