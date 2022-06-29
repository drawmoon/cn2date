from cn2date.nl.decorators import SelectorMethod
from cn2date.nl.selector import SelectorSetBase
from cn2date.transform_info import TransformInfo
from cn2date.util import date_add, date_sub, endof, now, startof


class QuarterSelectorSet(SelectorSetBase):
    """
    季度 选择器集
    """

    def __init__(self):
        """
        初始化 QuarterSelectorCluster 类的新实例
        """
        super(QuarterSelectorSet, self).__init__()

    @staticmethod
    @SelectorMethod("本季度")
    def _s_1(transform_info: TransformInfo) -> bool:
        """

        :param transform_info:
        :return:
        """
        s = startof(now(), "q")
        e = endof(s, "q")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod("上季度")
    def _s_2(transform_info: TransformInfo) -> bool:
        """

        :param transform_info:
        :return:
        """
        s = date_sub(startof(now(), "q"), 1, "q")
        e = endof(s, "q")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod("下季度")
    def _s_3(transform_info: TransformInfo) -> bool:
        """

        :param transform_info:
        :return:
        """
        s = date_add(startof(now(), "q"), 1, "q")
        e = endof(s, "q")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod(":ARG:季度")
    def _s_4(transform_info: TransformInfo) -> bool:
        """

        :param transform_info:
        :return:
        """
        if transform_info.args is None or not any(transform_info.args):
            transform_info.errs.append("Missing parameters")
            return False

        default = transform_info.args[0]
        if default == 1:
            # 处理 "一季度" 字符串
            s = startof(now(), "fq")
            e = endof(s, "fq")
            transform_info.write(s, e)
        elif default == 2:
            # 处理 "二季度" 字符串
            s = startof(now(), "sq")
            e = endof(s, "sq")
            transform_info.write(s, e)
        elif default == 3:
            # 处理 "三季度" 字符串
            s = startof(now(), "tq")
            e = endof(s, "tq")
            transform_info.write(s, e)
        elif default == 4:
            # 处理 "四季度" 字符串
            s = startof(now(), "foq")
            e = endof(s, "foq")
            transform_info.write(s, e)
        else:
            return False

        return True

    @staticmethod
    @SelectorMethod("前:ARG:季度")
    def _s_5(transform_info: TransformInfo) -> bool:
        """

        例如:
            当前时间 2021/10/1，前两季度，即 2021/4/1 - 2021/10/1

        :param transform_info:
        :return:
        """
        if transform_info.args is None or not any(transform_info.args):
            transform_info.errs.append("Missing parameters")
            return False

        s = date_sub(startof(now(), "q"), transform_info.args[0], "q")
        e = startof(now(), "q")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod("后:ARG:季度")
    def _s_6(transform_info: TransformInfo) -> bool:
        """

        例如:
            当前时间 2021/10/1，后两季度，即 2022/1/1 - 2022/7/1

        :param transform_info:
        :return:
        """
        if transform_info.args is None or not any(transform_info.args):
            transform_info.errs.append("Missing parameters")
            return False

        s = date_add(startof(now(), "q"), 1, "q")
        e = date_add(s, transform_info.args[0], "q")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod(":ARG:季度前")
    def _s_7(transform_info: TransformInfo) -> bool:
        """

        例如:
            当前时间 2021/10/1，两季度前，即 2021/4/1 - 2021/7/1

        :param transform_info:
        :return:
        """
        if transform_info.args is None or not any(transform_info.args):
            transform_info.errs.append("Missing parameters")
            return False

        s = date_sub(startof(now(), "q"), transform_info.args[0], "q")
        e = endof(s, "q")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod(":ARG:季度后")
    def _s_8(transform_info: TransformInfo) -> bool:
        """

        例如:
            当前时间 2021/10/1，两季度后，即 2022/4/1 - 2022/7/1

        :param transform_info:
        :return:
        """
        if transform_info.args is None or not any(transform_info.args):
            transform_info.errs.append("Missing parameters")
            return False

        s = date_add(startof(now(), "q"), transform_info.args[0], "q")
        e = endof(s, "q")
        transform_info.write(s, e)
        return True

    @staticmethod
    @SelectorMethod(":ARG:季度内")
    def _s_9(transform_info: TransformInfo) -> bool:
        """

        例如:
            当前时间 2021/10/1，两季度内，即 2021/7/1 - 2022/1/1

        :param transform_info:
        :return:
        """
        if transform_info.args is None or not any(transform_info.args):
            transform_info.errs.append("Missing parameters")
            return False

        s = date_sub(startof(now(), "q"), transform_info.args[0] - 1, "q")
        e = date_add(startof(now(), "q"), 1, "q")
        transform_info.write(s, e)
        return True
