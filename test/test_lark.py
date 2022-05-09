from test.util import get_node_value

import pytest
from lark import Lark


def __test(g: str, matched, unmatched):
    l = Lark(g)

    for i in matched:
        print("input", i)

        t = l.parse(i)
        assert t is not None

        days_val = get_node_value(t, "date")
        print("output", days_val)
        assert days_val == i

    for i in unmatched:
        with pytest.raises(Exception):
            l.parse(i)


def __simple_transform(n: str, cast_chart_ten = False) -> str:
    _0 = "零"
    _1 = "一"
    _10 = "十"
    t = { "0": _0, "1": _1, "2": "二", "3": "三", "4": "四", "5": "五", "6": "六", "7": "七", "8": "八", "9": "九" }
    
    val = n.translate(str.maketrans(t))

    if cast_chart_ten and len(val) == 2 and val[0] != _0:
        val = f"{val[0]}{_10}" if val[1] == _0 else f"{val[0]}{_10}{val[1]}"
        return val[1:] if val[0] == _1 else val
    return val


def test_year_lark():
    _01_99 = [str(i).rjust(2, "0") for i in list(range(1, 100))]
    _1000_9999 = [str(i) for i in list(range(1000, 10000))]
    _01_99_1000_9999 = _01_99 + _1000_9999
    _01_99_1000_9999_cn = [__simple_transform(i) for i in _01_99_1000_9999]

    matched = _01_99_1000_9999 + _01_99_1000_9999_cn + ["二0二二", "0一"]
    unmatched = ["0", "1", "111", "零", "一", "十", "十三", "一一一"]

    g = """
        start: date

        date: _year_2
            | _year_4

        _year_4: ONE_NINE ZERO_NINE ZERO_NINE ZERO_NINE
        _year_2: ZERO_NINE ZERO_NINE

        ZERO_NINE: /[0-9零一二三四五六七八九]/
        ONE_NINE: /[1-9一二三四五六七八九]/
    """

    __test(g, matched, unmatched)


def test_month_lark():
    _1_9 = [str(i) for i in list(range(1, 10))]
    _01_09 = [f"0{i}" for i in _1_9]
    _10_12 = [str(i) for i in list(range(10, 13))]
    _01_09_1_12 = _1_9 + _10_12 + _01_09
    _01_09_1_12_cn = [__simple_transform(i) for i in _01_09_1_12] + [__simple_transform(i, True) for i in _10_12]

    matched = _01_09_1_12 + _01_09_1_12_cn + ["一2", "十2"]
    unmatched = ["0", "13", "111", "零", "一三", "十三", "十十", "一十", "一十一", "一一一"]

    g = """
        start: date

        date: _month_1_9
            | _month_01_09
            | _month_10_12

        _month_10_12: /[1一]/ /[0-2零一二]/
                    | /十/ /[12一二]/?
        _month_01_09: /[0零]/ _month_1_9
        _month_1_9  : ONE_NINE

        ZERO_NINE: /[0-9零一二三四五六七八九]/
        ONE_NINE: /[1-9一二三四五六七八九]/
    """

    __test(g, matched, unmatched)


def test_day_lark():
    _1_9 = [str(i) for i in list(range(1, 10))]
    _01_09 = [f"0{i}" for i in _1_9]
    _10_31 = [str(i) for i in list(range(10, 32))]
    _01_09_1_31 = _1_9 + _10_31 + _01_09
    _01_09_1_31_cn = [__simple_transform(i) for i in _01_09_1_31] + [__simple_transform(i, True) for i in _10_31]

    matched = _01_09_1_31 + _01_09_1_31_cn + ["一3", "十3", "3十1"]
    unmatched = ["0", "32", "011", "111", "零", "三二", "三十二", "零十", "十零", "十十", "一十", "一十一", "一一一"]

    g = """
        start: date

        date: _day_1_9
            | _day_01_09
            | _day_10_29
            | _day_30_31

        _day_30_31: /[3三]/ (/[01零一]/ | /十/ /[1一]/?)
        _day_10_29: /[12一二]/ ZERO_NINE
                    | /[2二]/? /十/
                    | /[2二]/? /十/ ONE_NINE
        _day_01_09: /[0零]/ _day_1_9
        _day_1_9  : ONE_NINE

        ZERO_NINE: /[0-9零一二三四五六七八九]/
        ONE_NINE: /[1-9一二三四五六七八九]/
    """

    __test(g, matched, unmatched)
