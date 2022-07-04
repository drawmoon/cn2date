from cn2date.nl.decorators import SelectorMethod
from cn2date.nl.selector import SelectorSetBase
from cn2date.transform_info import TransformInfo
from cn2date.util import date_add, date_sub, endof, now, startof


class MonthSelectorSet(SelectorSetBase):
    """
    月 选择器集
    """

    def __init__(self):
        """
        初始化 MonthSelectorSet 类的新实例
        """
        super(MonthSelectorSet, self).__init__()

    @staticmethod
    @SelectorMethod("本月")
    def _s_1(transform_info: TransformInfo) -> bool:
        """

        :param transform_info:
        :return:
        """
        s = startof(now(), "m")
        e = endof(s, "m")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod("下月")
    def _s_2(transform_info: TransformInfo) -> bool:
        """

        :param transform_info:
        :return:
        """
        s = date_add(startof(now(), "m"), 1, "m")
        e = endof(s, "m")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod("上月")
    def _s_3(transform_info: TransformInfo) -> bool:
        """

        :param transform_info:
        :return:
        """
        s = date_sub(startof(now(), "m"), 1, "m")
        e = endof(s, "m")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod("前:ARG:月")
    def _s_4(transform_info: TransformInfo) -> bool:
        """

        例如:
            当前时间 2021/10/1，前三月，即 2021/7/1 00:00:00 - 2021/10/1 00:00:00

        :param transform_info:
        :return:
        """
        if transform_info.args is None or not any(transform_info.args):
            transform_info.errs.append("Missing parameters")
            return False

        s = date_sub(startof(now(), "m"), transform_info.args[0], "m")
        e = startof(now(), "m")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod("后:ARG:月")
    def _s_5(transform_info: TransformInfo) -> bool:
        """

        例如:
            当前时间 2021/10/1，后三月，即 2021/11/1 00:00:00 - 2022/2/1 00:00:00

        :param transform_info:
        :return:
        """
        if transform_info.args is None or not any(transform_info.args):
            transform_info.errs.append("Missing parameters")
            return False

        s = date_add(startof(now(), "m"), 1, "m")
        e = date_add(s, transform_info.args[0], "m")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod(":ARG:月前")
    def _s_6(transform_info: TransformInfo) -> bool:
        """

        例如:
            当前时间 2021/10/1，三月前，即 2021/7/1 00:00:00 - 2021/8/1 00:00:00

        :param transform_info:
        :return:
        """
        if transform_info.args is None or not any(transform_info.args):
            transform_info.errs.append("Missing parameters")
            return False

        s = date_sub(startof(now(), "m"), transform_info.args[0], "m")
        e = endof(s, "m")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod(":ARG:月后")
    def _s_7(transform_info: TransformInfo) -> bool:
        """

        例如:
            当前时间 2021/10/1，三月后，即 2022/1/1 00:00:00 - 2022/2/1 00:00:00

        :param transform_info:
        :return:
        """
        if transform_info.args is None or not any(transform_info.args):
            transform_info.errs.append("Missing parameters")
            return False

        s = date_add(startof(now(), "m"), transform_info.args[0], "m")
        e = endof(s, "m")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod(":ARG:月内")
    def _s_8(transform_info: TransformInfo) -> bool:
        """

        例如:
            当前时间 2021/10/1，三月内，即 2021/8/1 00:00:00 - 2021/11/1 00:00:00

        :param transform_info:
        :return:
        """
        if transform_info.args is None or not any(transform_info.args):
            transform_info.errs.append("Missing parameters")
            return False

        s = date_sub(startof(now(), "m"), transform_info.args[0] - 1, "m")
        e = date_add(startof(now(), "m"), 1, "m")
        transform_info.write(s, e)
        return True
