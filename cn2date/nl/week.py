from cn2date.nl.decorators import SelectorMethod
from cn2date.nl.selector import SelectorSetBase
from cn2date.transform_info import TransformInfo
from cn2date.util import date_add, date_sub, endof, now, startof


class WeekSelectorSet(SelectorSetBase):
    """
    周/星期 选择器集
    """

    def __init__(self):
        """
        初始化 WeekSelectorSet 类的新实例
        """
        self._synonym = {"周": ["星期"]}
        super(WeekSelectorSet, self).__init__()

    @staticmethod
    @SelectorMethod("本周")
    def _s_1(transform_info: TransformInfo) -> bool:
        """

        :param transform_info:
        :return:
        """
        s = startof(now(), "w")
        e = endof(s, "w")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod("上周")
    def _s_2(transform_info: TransformInfo) -> bool:
        """

        :param transform_info:
        :return:
        """
        s = date_sub(startof(now(), "w"), 1, "w")
        e = endof(s, "w")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod("下周")
    def _s_3(transform_info: TransformInfo) -> bool:
        """

        :param transform_info:
        :return:
        """
        s = date_add(startof(now(), "w"), 1, "w")
        e = endof(s, "w")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod("前:ARG:周")
    def _s_4(transform_info: TransformInfo) -> bool:
        """

        例如:
            当前时间 2021/10/1，前三周，即 2021/9/6 00:00:00 - 2021/9/27 00:00:00

        :param transform_info:
        :return:
        """
        if transform_info.args is None or not any(transform_info.args):
            transform_info.errs.append("Missing parameters")
            return False

        s = date_sub(startof(now(), "w"), transform_info.args[0], "w")
        e = startof(now(), "w")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod("后:ARG:周")
    def _s_5(transform_info: TransformInfo) -> bool:
        """

        例如:
            当前时间 2021/10/1，后三周，即 2021/10/4 00:00:00 - 2021/10/25 00:00:00

        :param transform_info:
        :return:
        """
        if transform_info.args is None or not any(transform_info.args):
            transform_info.errs.append("Missing parameters")
            return False

        s = date_add(startof(now(), "w"), 1, "w")
        e = date_add(s, transform_info.args[0], "w")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod(":ARG:周前")
    def _s_6(transform_info: TransformInfo) -> bool:
        """

        例如:
            当前时间 2021/10/1，三周前，即 2021/9/6 00:00:00 - 2021/9/13 00:00:00

        :param transform_info:
        :return:
        """
        if transform_info.args is None or not any(transform_info.args):
            transform_info.errs.append("Missing parameters")
            return False

        s = date_sub(startof(now(), "w"), transform_info.args[0], "w")
        e = endof(s, "w")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod(":ARG:周后")
    def _s_7(transform_info: TransformInfo) -> bool:
        """

        例如:
            当前时间 2021/10/1，三周后，即 2021/10/18 00:00:00 - 2021/10/25 00:00:00

        :param transform_info:
        :return:
        """
        if transform_info.args is None or not any(transform_info.args):
            transform_info.errs.append("Missing parameters")
            return False

        s = date_add(startof(now(), "w"), transform_info.args[0], "w")
        e = endof(s, "w")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod(":ARG:周内")
    def _s_8(transform_info: TransformInfo) -> bool:
        """

        例如:
            当前时间 2021/10/1，三周内，即 2021/9/13 00:00:00 - 2021/10/4 00:00:00

        :param transform_info:
        :return:
        """
        if transform_info.args is None or not any(transform_info.args):
            transform_info.errs.append("Missing parameters")
            return False

        s = date_sub(startof(now(), "w"), transform_info.args[0] - 1, "w")
        e = date_add(startof(now(), "w"), 1, "w")
        transform_info.write(s, e)
        return True
