from __future__ import annotations

from cn2date.nl.decorators import SelectorMethod
from cn2date.nl.selector import SelectorBase
from cn2date.transform_info import TransformInfo
from cn2date.util import date_add, date_sub, endof, now, startof


class YearSelector(SelectorBase):
    """ """

    @SelectorMethod("今年")
    def _s_1(self, transform_info: TransformInfo) -> bool:
        """
        今年

        :param transform_info:
        :return:
        """
        s = startof(now(), "y")
        e = endof(s, "y")
        transform_info.write(s, e)
        return True

    @SelectorMethod("明年")
    def _s_2(self, transform_info: TransformInfo) -> bool:
        """
        明年

        :param transform_info:
        :return:
        """
        s = date_add(startof(now(), "y"), 1, "y")
        e = endof(s, "y")
        transform_info.write(s, e)
        return True

    @SelectorMethod("去年")
    def _s_3(self, transform_info: TransformInfo) -> bool:
        """
        去年

        :param transform_info:
        :return:
        """
        s = date_sub(startof(now(), "y"), 1, "y")
        e = endof(s, "y")
        transform_info.write(s, e)
        return True

    @SelectorMethod("前年")
    def _s_4(self, transform_info: TransformInfo) -> bool:
        """
        前年

        :param transform_info:
        :return:
        """
        s = date_sub(startof(now(), "y"), 2, "y")
        e = endof(s, "y")
        transform_info.write(s, e)
        return True

    @SelectorMethod("上半年")
    def _s_5(self, transform_info: TransformInfo) -> bool:
        """
        上半年

        :param transform_info:
        :return:
        """
        s = startof(now(), "fhoy")
        e = endof(s, "fhoy")
        transform_info.write(s, e)
        return True

    @SelectorMethod("下半年")
    def _s_6(self, transform_info: TransformInfo) -> bool:
        """
        下半年

        :param transform_info:
        :return:
        """
        s = startof(now(), "shoy")
        e = endof(s, "shoy")
        transform_info.write(s, e)
        return True

    @SelectorMethod("前几年")
    def _s_7(self, transform_info: TransformInfo) -> bool:
        """
        前几年

        例如：
            当前时间 2021/1/1，前三年，即 2018/1/1 - 2021/1/1

        :param transform_info:
        :return:
        """
        pass

    @SelectorMethod("后几年")
    def _s_8(self, transform_info: TransformInfo) -> bool:
        """
        后几年

        例如：
            当前时间 2021/1/1，后三年，即 2022/1/1 - 2025/1/1

        :param transform_info:
        :return:
        """
        pass

    @SelectorMethod("几年前")
    def _s_9(self, transform_info: TransformInfo) -> bool:
        """
        几年前

        例如：
            当前时间 2021/1/1，三年前，即 2018/1/1 - 2019/1/1

        :param transform_info:
        :return:
        """
        pass

    @SelectorMethod("几年后")
    def _s_10(self, transform_info: TransformInfo) -> bool:
        """
        几年后

        例如：
            当前时间 2021/1/1，三年后，即 2024/1/1 - 2025/1/1

        :param transform_info:
        :return:
        """
        pass

    @SelectorMethod("几年内")
    def _s_11(self, transform_info: TransformInfo) -> bool:
        """
        几年内

        例如：
            当前时间 2021/1/1，三年内，即 2019/1/1 - 2022/1/1

        :param transform_info:
        :return:
        """
        pass
