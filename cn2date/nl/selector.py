# pyright: strict

from __future__ import annotations

import inspect
from typing import Callable, Optional

from cn2date.transform_info import TransformInfo
from cn2date.util import SimpleTransform, isblank


class SelectorPreDefinedVariable:
    """
    选择器的预定义变量

    参数:
        - arg: 表示此处为用作评估选择器的参数
    """

    arg = ":ARG:"
    variables = [arg]

    @staticmethod
    def parse(text: str) -> list[str]:
        """

        :param text:
        :return:
        """
        last_end = 0
        operator = -1

        items: list[str] = []
        for i, s in enumerate(text):
            if s == ":":
                if operator == -1:
                    if last_end != i:
                        items.append(text[last_end:i])

                    operator = i
                else:
                    items.append(text[operator : i + 1])
                    operator = -1

                last_end = i + 1
        else:
            items.append(text[last_end : len(text)])

        return items

    @staticmethod
    def is_variable(text: str) -> bool:
        """

        :param text:
        :return:
        """
        return text[0] == ":" and text[::-1][0] == ":"


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
        if isblank(transform_info.current) or self.synonym is None:
            return

        for k, arr in self.synonym.items():
            for s in arr:
                transform_info.current = transform_info.current.replace(s, k)

    def _handle_variable(self, transform_info: TransformInfo) -> None:
        """
        处理预定义变量

        :param transform_info:
        """
        if isblank(transform_info.current):
            return

        for var in SelectorPreDefinedVariable.variables:
            if var in self.name:
                # 提取预定义变量占位符处的值，并将该值替换为预定义变量占位符
                # 例如："前30天" 处理完后的结果为 ["前:ARG:天", 30]
                current = transform_info.current

                # 尝试解析 Selector.name
                items = SelectorPreDefinedVariable.parse(self.name)

                try:
                    # 尝试查找参数
                    args: list[str] = []

                    index = 0
                    last_end = -1

                    for item in items:
                        if SelectorPreDefinedVariable.is_variable(item):
                            last_end = index
                        else:
                            if last_end != -1:
                                args.append(current[last_end : current.index(item)])
                            index = current.index(item) + len(item)
                            if index >= len(current):
                                break

                    for arg in args:
                        # 尝试将预定义变量占位符处的值添加到 transform_info.args 中
                        transform_info.args.append(int(SimpleTransform().cn2numstr(arg)))

                        # 设置处理完成后的当前值
                        transform_info.current = transform_info.current.replace(arg, var)
                except ValueError:
                    pass

    def __match(self, transform_info: TransformInfo) -> bool:
        """
        匹配当前选择器是否能够处理当前值

        :param transform_info:
        :return: 如果匹配成功，则返回 True，否则返回 False
        """
        if isblank(transform_info.current):
            return False
        return self.__rule(transform_info.current) if self.__rule is not None else transform_info.current == self.name

    def eval(self, transform_info: TransformInfo) -> bool:
        """
        根据 TransformInfo.current 评估选择器

        :param transform_info:
        :return: 如果可以评估选择器，将返回 True，否则返回 False
        """
        if isblank(transform_info.current):
            return False

        original = transform_info.current

        # 处理代名词
        self._handle_synonym(transform_info)
        # 处理预定义变量
        self._handle_variable(transform_info)

        if not self.__match(transform_info):
            transform_info.current = original
            return False

        return self.__fn(transform_info)


class SelectorSetBase:
    """
    选择器集的基类

    继承 SelectorClusterBase 类，在初始化类时会自动将类下标记 @SelectorMethod 装饰器的方法
    转换为 Selector 并添加到 items 集合中
    """

    items: list[Selector]
    _synonym: dict[str, list[str]] | None = None

    def __init__(self) -> None:
        """
        初始化 SelectorClusterBase 类的新实例
        """
        self.items = []

        # 自动注册标记 @SelectorMethod 装饰器的方法
        for (_, m) in inspect.getmembers(self, inspect.isfunction):
            if "__selector__" in m.__dict__:
                self.__safe_add(m.__dict__["__selector__"])

    def __safe_add(self, selector: Selector) -> None:
        """
        安全的添加选择器

        如果设置了代名词，则会在添加选择器时，同时设置选择器的代名词

        :param selector: 选择器
        :except ValueError: 当相同名称的选择器重复添加时，则会引发 ValueError 错误
        """
        if selector.name in [s.name for s in self.items]:
            raise ValueError(f"Same key already exist: {selector.name}")
        if self._synonym is not None:
            selector.synonym = dict(selector.synonym, **self._synonym)
        self.items.append(selector)
