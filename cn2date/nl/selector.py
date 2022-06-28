# pyright: strict

from __future__ import annotations

import inspect
from typing import Callable, Optional

from cn2date.transform_info import TransformInfo
from cn2date.util import _SimpleTransform


class SelectorPreDefinedVariable:
    """
    选择器的预定义变量

    参数:
        - arg: 表示此处为用作评估选择器的参数
    """

    arg = ":ARG:"
    variables = [arg]


class Selector:
    """
    选择器
    """

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
        初始化 Selector 类的新实例

        :param name: 选择器的名称
        :param fn: 用作评估选择器的具体实现
        :param rule: 匹配选择器的自定义规则
        :param synonym: 用于处理 TransformInfo.current 的代名词
        """
        self.name = name
        self.__fn = fn
        self.__rule = rule
        if synonym is not None:
            self.synonym = dict(self.synonym, **synonym)

    def _handle_synonym(self, transform_info: TransformInfo) -> None:
        """
        处理代名词

        :param transform_info:
        """
        if self.synonym is None:
            return

        for k, arr in self.synonym.items():
            for s in arr:
                transform_info.current = transform_info.current.replace(s, k)

    def _handle_variable(self, transform_info: TransformInfo) -> None:
        """
        处理预定义变量

        :param transform_info:
        """
        for var in SelectorPreDefinedVariable.variables:
            if var in self.name:
                # 提取预定义变量占位符处的值，并将该值替换为预定义变量占位符
                # 例如："前30天" 处理完后的结果为 ["前:ARG:天", 30]
                head = self.name.index(var)
                tail = self.name[::-1].index(var[::-1])

                s = transform_info.current.replace(transform_info.current[0:head], "")[::-1]
                s = s.replace(s[0:tail], "")[::-1]

                # 尝试将预定义变量占位符处的值添加到 transform_info.args 中
                try:
                    transform_info.args.append(int(_SimpleTransform().cn2numstr(s)))
                except ValueError:
                    pass

                # 设置处理完成后的当前值
                transform_info.current = transform_info.current.replace(s, var)

    def __match(self, transform_info: TransformInfo) -> bool:
        """
        匹配当前选择器是否能够处理当前值

        :param transform_info:
        :return: 如果匹配成功，则返回 True，否则返回 False
        """
        return self.__rule(transform_info.current) if self.__rule is not None else transform_info.current == self.name

    def eval(self, transform_info: TransformInfo) -> bool:
        """
        根据 TransformInfo.current 评估选择器

        :param transform_info:
        :return: 如果可以评估选择器，将返回 True，否则返回 False
        """
        original = transform_info.current

        # 处理代名词
        self._handle_synonym(transform_info)
        # 处理预定义变量
        self._handle_variable(transform_info)

        if not self.__match(transform_info):
            transform_info.current = original
            return False

        return self.__fn(transform_info)


class SelectorClusterBase:
    """
    选择器簇的基类

    继承 SelectorClusterBase 类，在初始化类时会自动将类下标记 @SelectorMethod 装饰器的方法
    转换为 Selector 并添加到 selectors 集合中
    """

    selectors: list[Selector] = []
    _synonym: dict[str, list[str]] | None = None

    def __init__(self) -> None:
        """
        初始化 SelectorClusterBase 类的新实例
        """
        # 自动注册标记 @SelectorMethod 装饰器的方法
        fn_list = inspect.getmembers(self, inspect.isfunction)
        for (_, m) in fn_list:
            if "__selector__" in m.__dict__:
                self.__safe_add(m.__dict__["__selector__"])

    def __safe_add(self, selector: Selector) -> None:
        """
        安全的添加选择器

        如果设置了代名词，则会在添加选择器时，同时设置选择器的代名词

        :param selector: 选择器
        :except ValueError: 当相同名称的选择器重复添加时，则会引发 ValueError 错误
        """
        if selector.name in [s.name for s in self.selectors]:
            raise ValueError(f"Same key already exist: {selector.name}")
        if self._synonym is not None:
            selector.synonym = dict(selector.synonym, **self._synonym)
        self.selectors.append(selector)
