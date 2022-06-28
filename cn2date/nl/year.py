# pyright: strict

from __future__ import annotations

from cn2date.nl.decorators import SelectorMethod
from cn2date.nl.selector import SelectorClusterBase
from cn2date.transform_info import TransformInfo
from cn2date.util import date_add, date_sub, endof, now, startof


class YearSelectorCluster(SelectorClusterBase):
    """ """

    def __init__(self):
        self._synonym = {"今": ["本"], "去年": ["上年"], "明年": ["下年"]}
        super(YearSelectorCluster, self).__init__()

    @staticmethod
    @SelectorMethod("今年")
    def _s_1(transform_info: TransformInfo) -> bool:
        """
        今年

        :param transform_info:
        :return:
        """
        s = startof(now(), "y")
        e = endof(s, "y")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod("明年")
    def _s_2(transform_info: TransformInfo) -> bool:
        """
        明年

        :param transform_info:
        :return:
        """
        s = date_add(startof(now(), "y"), 1, "y")
        e = endof(s, "y")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod("去年")
    def _s_3(transform_info: TransformInfo) -> bool:
        """
        去年

        :param transform_info:
        :return:
        """
        s = date_sub(startof(now(), "y"), 1, "y")
        e = endof(s, "y")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod("前年")
    def _s_4(transform_info: TransformInfo) -> bool:
        """
        前年

        :param transform_info:
        :return:
        """
        s = date_sub(startof(now(), "y"), 2, "y")
        e = endof(s, "y")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod("上半年")
    def _s_5(transform_info: TransformInfo) -> bool:
        """
        上半年

        :param transform_info:
        :return:
        """
        s = startof(now(), "fhoy")
        e = endof(s, "fhoy")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod("下半年")
    def _s_6(transform_info: TransformInfo) -> bool:
        """
        下半年

        :param transform_info:
        :return:
        """
        s = startof(now(), "shoy")
        e = endof(s, "shoy")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod("前:ARG:年")
    def _s_7(transform_info: TransformInfo) -> bool:
        """
        前几年

        例如：
            当前时间 2021/1/1，前三年，即 2018/1/1 - 2021/1/1

        :param transform_info:
        :return:
        """
        if transform_info.args is None or not any(transform_info.args):
            transform_info.errs.append("Missing parameters")
            return False

        s = date_sub(startof(now(), "y"), transform_info.args[0], "y")
        e = startof(now(), "y")
        transform_info.write(s, e)

        return True

    @staticmethod
    @SelectorMethod("后:ARG:年")
    def _s_8(transform_info: TransformInfo) -> bool:
        """
        后几年

        例如：
            当前时间 2021/1/1，后三年，即 2022/1/1 - 2025/1/1

        :param transform_info:
        :return:
        """
        if transform_info.args is None or not any(transform_info.args):
            transform_info.errs.append("Missing parameters")
            return False

        s = date_add(startof(now(), "y"), 1, "y")
        e = date_add(s, transform_info.args[0], "y")
        transform_info.write(s, e)

        return True

    @staticmethod
    @SelectorMethod(":ARG:年前")
    def _s_9(transform_info: TransformInfo) -> bool:
        """
        几年前

        例如：
            当前时间 2021/1/1，三年前，即 2018/1/1 - 2019/1/1

        :param transform_info:
        :return:
        """
        if transform_info.args is None or not any(transform_info.args):
            transform_info.errs.append("Missing parameters")
            return False

        s = date_sub(startof(now(), "y"), transform_info.args[0], "y")
        e = endof(s, "y")
        transform_info.write(s, e)

        return True

    @staticmethod
    @SelectorMethod(":ARG:年后")
    def _s_10(transform_info: TransformInfo) -> bool:
        """
        几年后

        例如：
            当前时间 2021/1/1，三年后，即 2024/1/1 - 2025/1/1

        :param transform_info:
        :return:
        """
        if transform_info.args is None or not any(transform_info.args):
            transform_info.errs.append("Missing parameters")
            return False

        s = date_add(startof(now(), "y"), transform_info.args[0], "y")
        e = endof(s, "y")
        transform_info.write(s, e)

        return True

    @staticmethod
    @SelectorMethod(":ARG:年内")
    def _s_11(transform_info: TransformInfo) -> bool:
        """
        几年内

        例如：
            当前时间 2021/1/1，三年内，即 2019/1/1 - 2022/1/1

        :param transform_info:
        :return:
        """
        if transform_info.args is None or not any(transform_info.args):
            transform_info.errs.append("Missing parameters")
            return False

        s = date_sub(startof(now(), "y"), transform_info.args[0] - 1, "y")
        e = date_add(startof(now(), "y"), 1, "y")
        transform_info.write(s, e)

        return True
