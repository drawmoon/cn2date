from cn2date.nl.decorators import SelectorMethod
from cn2date.nl.selector import SelectorSetBase
from cn2date.transform_info import TransformInfo
from cn2date.util import date_add, date_sub, endof, now, startof


class DaySelectorSet(SelectorSetBase):
    """
    日/天 选择器集
    """

    def __init__(self):
        """
        初始化 DaySelectorSet 类的新实例
        """
        self._synonym = {"天": ["日"]}
        super(DaySelectorSet, self).__init__()

    @staticmethod
    @SelectorMethod("今天")
    def _s_1(transform_info: TransformInfo) -> bool:
        """

        :param transform_info:
        :return:
        """
        s = startof(now(), "d")
        e = endof(s, "d")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod("明天")
    def _s_2(transform_info: TransformInfo) -> bool:
        """

        :param transform_info:
        :return:
        """
        s = date_add(startof(now(), "d"), 1, "d")
        e = endof(s, "d")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod("后天")
    def _s_3(transform_info: TransformInfo) -> bool:
        """

        :param transform_info:
        :return:
        """
        s = date_add(startof(now(), "d"), 2, "d")
        e = endof(s, "d")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod("昨天")
    def _s_4(transform_info: TransformInfo) -> bool:
        """

        :param transform_info:
        :return:
        """
        s = date_sub(startof(now(), "d"), 1, "d")
        e = endof(s, "d")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod("前天")
    def _s_5(transform_info: TransformInfo) -> bool:
        """

        :param transform_info:
        :return:
        """
        s = date_sub(startof(now(), "d"), 2, "d")
        e = endof(s, "d")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod("上午")
    def _s_6(transform_info: TransformInfo) -> bool:
        """

        :param transform_info:
        :return:
        """
        s = startof(now(), "am")
        e = endof(s, "am")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod("下午")
    def _s_7(transform_info: TransformInfo) -> bool:
        """

        :param transform_info:
        :return:
        """
        s = startof(now(), "pm")
        e = endof(s, "pm")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod("前:ARG:天")
    def _s_8(transform_info: TransformInfo) -> bool:
        """

        例如:
            当前时间 2021/10/1，前三天，即 2021/9/28 - 2021/10/1

        :param transform_info:
        :return:
        """
        if transform_info.args is None or not any(transform_info.args):
            transform_info.errs.append("Missing parameters")
            return False

        s = date_sub(startof(now(), "d"), transform_info.args[0], "d")
        e = startof(now(), "d")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod("后:ARG:天")
    def _s_9(transform_info: TransformInfo) -> bool:
        """

        例如:
            当前时间 2021/10/1，后三天，即 2021/10/2 - 2021/10/5

        :param transform_info:
        :return:
        """
        if transform_info.args is None or not any(transform_info.args):
            transform_info.errs.append("Missing parameters")
            return False

        s = date_add(startof(now(), "d"), 1, "d")
        e = date_add(s, transform_info.args[0], "d")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod(":ARG:天前")
    def _s_10(transform_info: TransformInfo) -> bool:
        """

        例如:
            当前时间 2021/10/1，三天前，即 2021/9/28 - 2021/9/29

        :param transform_info:
        :return:
        """
        if transform_info.args is None or not any(transform_info.args):
            transform_info.errs.append("Missing parameters")
            return False

        s = date_sub(startof(now(), "d"), transform_info.args[0], "d")
        e = endof(s, "d")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod(":ARG:天后")
    def _s_11(transform_info: TransformInfo) -> bool:
        """

        例如:
            当前时间 2021/10/1，三天后，即 2021/10/4 - 2021/10/5

        :param transform_info:
        :return:
        """
        if transform_info.args is None or not any(transform_info.args):
            transform_info.errs.append("Missing parameters")
            return False

        s = date_add(startof(now(), "d"), transform_info.args[0], "d")
        e = endof(s, "d")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod(":ARG:天内")
    def _s_12(transform_info: TransformInfo) -> bool:
        """

        例如:
            当前时间 2021/10/1，三天后，即 2021/10/4 - 2021/10/5

        :param transform_info:
        :return:
        """
        if transform_info.args is None or not any(transform_info.args):
            transform_info.errs.append("Missing parameters")
            return False

        s = date_add(startof(now(), "d"), transform_info.args[0], "d")
        e = endof(s, "d")
        transform_info.write(s, e)
        return True
