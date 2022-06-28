# pyright: strict

from __future__ import annotations

import inspect
from typing import Callable, Optional

from cn2date.transform_info import TransformInfo
from cn2date.util import _SimpleTransform


class SelectorPreDefinedVariable:
    arg = ":ARG:"
    variables = [arg]


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

    def __handle_variable(self, transform_info: TransformInfo) -> None:
        """

        :param transform_info:
        :return:
        """
        for var in SelectorPreDefinedVariable.variables:
            if var in self.name:
                # 提取预定义变量占位符处的值，并将该值替换为预定义变量占位符
                # 例如："前30天" 处理完后的结果为 ["前:ARG:天", 30]
                head = self.name.index(var)
                tail = self.name[::-1].index(var[::-1])

                s = transform_info.current.replace(transform_info.current[0:head], "")[::-1]
                s = s.replace(s[0:tail], "")[::-1]

                try:
                    transform_info.args.append(int(_SimpleTransform().cn2numstr(s)))
                except ValueError:
                    pass

                transform_info.current = transform_info.current.replace(s, var)

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
        original = transform_info.current

        # 处理代名词
        self.__handle_synonym(transform_info)
        # 处理预定义变量
        self.__handle_variable(transform_info)

        if not self.__match(transform_info):
            transform_info.current = original
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
