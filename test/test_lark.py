from pathlib import Path
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
    

file = Path(__file__).parent.parent / "cn2date/date.lark"
file_text = open(file, "r", encoding="utf-8").read()
grammars = file_text.split("===")

date_parser = Lark(grammars[0])
nl_parser = Lark(grammars[1])


date_testdata = [
    # 完整的日期格式
    ("2021-9-10", "2021", "9", "10"),
    ("2021-09-10", "2021", "09", "10"),
    ("2021-09-1", "2021", "09", "1"),
    ("2021-9-1", "2021", "9", "1"),
    ("21-9-10", "21", "9", "10"),
    ("21-09-10", "21", "09", "10"),
    ("21-09-1", "21", "09", "1"),
    ("21-9-1", "21", "9", "1"),
    ("2021/9/10", "2021", "9", "10"),
    ("2021/09/10", "2021", "09", "10"),
    ("2021/09/1", "2021", "09", "1"),
    ("2021/9/1", "2021", "9", "1"),
    ("21/9/10", "21", "9", "10"),
    ("21/09/10", "21", "09", "10"),
    ("21/09/1", "21", "09", "1"),
    ("21/9/1", "21", "9", "1"),
    ("2021年9月10日", "2021", "9", "10"),
    ("2021年09月10日", "2021", "09", "10"),
    ("2021年09月10", "2021", "09", "10"),
    ("2021年09月1", "2021", "09", "1"),
    ("2021年9月1", "2021", "9", "1"),
    ("21年9月10日", "21", "9", "10"),
    ("21年09月10日", "21", "09", "10"),
    ("21年09月10", "21", "09", "10"),
    ("21年09月1", "21", "09", "1"),
    ("21年9月1", "21", "9", "1"),
    ("二零二一/九/三十一", "二零二一", "九", "三十一"),
    ("二零二一/九/十", "二零二一", "九", "十"),
    ("二零二一/零九/十", "二零二一", "零九", "十"),
    ("二零二一/零九/一", "二零二一", "零九", "一"),
    ("二零二一/九/一", "二零二一", "九", "一"),
    ("二一/九/十", "二一", "九", "十"),
    ("二一/零九/十", "二一", "零九", "十"),
    ("二一/零九/一", "二一", "零九", "一"),
    ("二一/九/一", "二一", "九", "一"),
    ("二零二一-九-三十一", "二零二一", "九", "三十一"),
    ("二零二一-九-十", "二零二一", "九", "十"),
    ("二零二一-零九-十", "二零二一", "零九", "十"),
    ("二零二一-零九-一", "二零二一", "零九", "一"),
    ("二零二一-九-一", "二零二一", "九", "一"),
    ("二一-九-十", "二一", "九", "十"),
    ("二一-零九-十", "二一", "零九", "十"),
    ("二一-零九-一", "二一", "零九", "一"),
    ("二一-九-一", "二一", "九", "一"),
    ("二零二一年九月三十一日", "二零二一", "九", "三十一"),
    ("二零二一年九月三十一号", "二零二一", "九", "三十一"),
    ("二零二一年九月三十一", "二零二一", "九", "三十一"),
    ("二零二一年九月十日", "二零二一", "九", "十"),
    ("二零二一年零九月十日", "二零二一", "零九", "十"),
    ("二零二一年零九月十", "二零二一", "零九", "十"),
    ("二零二一年零九月一", "二零二一", "零九", "一"),
    ("二零二一年九月一", "二零二一", "九", "一"),
    ("二一年九月十日", "二一", "九", "十"),
    ("二一年零九月十日", "二一", "零九", "十"),
    ("二一年零九月十", "二一", "零九", "十"),
    ("二一年零九月一", "二一", "零九", "一"),
    ("二一年九月一", "二一", "九", "一"),
    ("二零二一年09月10号", "二零二一", "09", "10"),
    ("二零二一年09/10号", "二零二一", "09", "10"),
    ("二零二一/09月十号", "二零二一", "09", "十"),
    ("二零二一年09-十日", "二零二一", "09", "十"),
    ("二零二一年09-十号", "二零二一", "09", "十"),
    ("二零二一年09-十", "二零二一", "09", "十"),
    ("二零二一年09/10", "二零二一", "09", "10"),
    ("二零二一年09-10", "二零二一", "09", "10"),
    ("2021/九月10", "2021", "九", "10"),
    ("2021/9月十", "2021", "9", "十"),
    ("2021年9月10号", "2021", "9", "10"),
    ("2021年09月10号", "2021", "09", "10"),
    ("21年9月10号", "21", "9", "10"),
    ("21年09月10号", "21", "09", "10"),
    ("二零二一年九月十号", "二零二一", "九", "十"),
    ("二零二一年零九月十号", "二零二一", "零九", "十"),
    ("二一年九月十号", "二一", "九", "十"),
    ("二一年零九月十号", "二一", "零九", "十"),
    # 只包含年的日期格式
    ("21年", "21", None, None),
    ("2021年", "2021", None, None),
    ("二一年", "二一", None, None),
    ("二零二一年", "二零二一", None, None),
    # 只包含年月的日期格式
    ("21-09", "21", "09", None),
    ("21/09", "21", "09", None),
    ("21年09月", "21", "09", None),
    ("21年9月", "21", "9", None),
    ("2021-09", "2021", "09", None),
    ("2021/09", "2021", "09", None),
    ("2021年09月", "2021", "09", None),
    ("2021年9月", "2021", "9", None),
    ("二一年零九月", "二一", "零九", None),
    ("二一年九月", "二一", "九", None),
    ("二零二一年零九月", "二零二一", "零九", None),
    ("二零二一年九月", "二零二一", "九", None),
    # 只包含月的日期格式
    ("1月", None, "1", None),
    ("01月", None, "01", None),
    ("12月", None, "12", None),
    ("一月", None, "一", None),
    ("零一月", None, "零一", None),
    ("十二月", None, "十二", None),
    ("一二月", None, "一二", None),
    # 只包含月日的日期格式
    ("9月10日", None, "9", "10"),
    ("09月10日", None, "09", "10"),
    ("09月1日", None, "09", "1"),
    ("9月1日", None, "9", "1"),
    ("9月10号", None, "9", "10"),
    ("09月10号", None, "09", "10"),
    ("09月1号", None, "09", "1"),
    ("9月1号", None, "9", "1"),
    ("九月十日", None, "九", "十"),
    ("零九月十日", None, "零九", "十"),
    ("零九月一日", None, "零九", "一"),
    ("九月一日", None, "九", "一"),
    ("九月十号", None, "九", "十"),
    ("零九月十号", None, "零九", "十"),
    ("零九月一号", None, "零九", "一"),
    ("九月一号", None, "九", "一"),
    # 只包含日的日期格式
    ("1日", None, None, "1"),
    ("01日", None, None, "01"),
    ("31日", None, None, "31"),
    ("一日", None, None, "一"),
    ("零一日", None, None, "零一"),
    ("三十一日", None, None, "三十一"),
    ("三一日", None, None, "三一"),
]


@pytest.mark.parametrize(
    "text,expected_years,expected_months,expected_days",
    date_testdata,
    ids=[i[0] for i in date_testdata],
)
def test_date_parse(
    text: str,
    expected_years: str,
    expected_months: str,
    expected_days: str,
):
    print("input", text)
    tree = date_parser.parse(text)

    assert tree is not None

    assert get_node_value(tree, "years") == expected_years
    assert get_node_value(tree, "months") == expected_months
    assert get_node_value(tree, "days") == expected_days


year_testdata = [
    (nl_parser, "今年", None, None, None, None, "今年"),
    (nl_parser, "本年", None, None, None, None, "本年"),
    (nl_parser, "本年份", None, None, None, None, "本年"),
    (nl_parser, "本年度", None, None, None, None, "本年"),
    (nl_parser, "当前年", None, None, None, None, "当前年"),
    (nl_parser, "当前年份", None, None, None, None, "当前年"),
    (nl_parser, "当前年度", None, None, None, None, "当前年"),
    (nl_parser, "明年", None, None, None, None, "明年"),
    (nl_parser, "去年", None, None, None, None, "去年"),
    (nl_parser, "前年", None, None, None, None, "前年"),
    (nl_parser, "上半年", None, None, None, None, "上半年"),
    (nl_parser, "下半年", None, None, None, None, "下半年"),
    (nl_parser, "前两年", None, None, None, None, "前两年"),
    (nl_parser, "前2年", None, None, None, None, "前2年"),
    (nl_parser, "前两个年", None, None, None, None, "前两年"),
    (nl_parser, "前2个年", None, None, None, None, "前2年"),
    (nl_parser, "前两个年份", None, None, None, None, "前两年"),
    (nl_parser, "前2个年份", None, None, None, None, "前2年"),
    (nl_parser, "两年前", None, None, None, None, "两年前"),
    (nl_parser, "2年前", None, None, None, None, "2年前"),
    (nl_parser, "两年内", None, None, None, None, "两年内"),
    (nl_parser, "2年内", None, None, None, None, "2年内"),
    (nl_parser, "两年以前", None, None, None, None, "两年以前"),
    (nl_parser, "2年以前", None, None, None, None, "2年以前"),
    (nl_parser, "两年之前", None, None, None, None, "两年之前"),
    (nl_parser, "2年之前", None, None, None, None, "2年之前"),
    (nl_parser, "两年以内", None, None, None, None, "两年以内"),
    (nl_parser, "2年以内", None, None, None, None, "2年以内"),
    (nl_parser, "两年之内", None, None, None, None, "两年之内"),
    (nl_parser, "2年之内", None, None, None, None, "2年之内"),
    (nl_parser, "两年以来", None, None, None, None, "两年以来"),
    (nl_parser, "2年以来", None, None, None, None, "2年以来"),
]

quarter_testdata = [
    (nl_parser, "本季度", None, None, None, None, "本季度"),
    (nl_parser, "这个季度", None, None, None, None, "这个季度"),
    (nl_parser, "当前季度", None, None, None, None, "当前季度"),
    (nl_parser, "上季度", None, None, None, None, "上季度"),
    (nl_parser, "上个季度", None, None, None, None, "上季度"),
    (nl_parser, "下季度", None, None, None, None, "下季度"),
    (nl_parser, "下个季度", None, None, None, None, "下季度"),
    (nl_parser, "第一季度", None, None, None, None, "一季度"),
    (nl_parser, "第一个季度", None, None, None, None, "一季度"),
    (nl_parser, "第1季度", None, None, None, None, "1季度"),
    (nl_parser, "第1个季度", None, None, None, None, "1季度"),
    (nl_parser, "一季度", None, None, None, None, "一季度"),
    (nl_parser, "1季度", None, None, None, None, "1季度"),
    (nl_parser, "第二季度", None, None, None, None, "二季度"),
    (nl_parser, "第二个季度", None, None, None, None, "二季度"),
    (nl_parser, "第2季度", None, None, None, None, "2季度"),
    (nl_parser, "第2个季度", None, None, None, None, "2季度"),
    (nl_parser, "2季度", None, None, None, None, "2季度"),
    (nl_parser, "二季度", None, None, None, None, "二季度"),
    (nl_parser, "第三季度", None, None, None, None, "三季度"),
    (nl_parser, "第三个季度", None, None, None, None, "三季度"),
    (nl_parser, "第3季度", None, None, None, None, "3季度"),
    (nl_parser, "第3个季度", None, None, None, None, "3季度"),
    (nl_parser, "三季度", None, None, None, None, "三季度"),
    (nl_parser, "3季度", None, None, None, None, "3季度"),
    (nl_parser, "第四季度", None, None, None, None, "四季度"),
    (nl_parser, "第四个季度", None, None, None, None, "四季度"),
    (nl_parser, "第4季度", None, None, None, None, "4季度"),
    (nl_parser, "第4个季度", None, None, None, None, "4季度"),
    (nl_parser, "四季度", None, None, None, None, "四季度"),
    (nl_parser, "4季度", None, None, None, None, "4季度"),
    (nl_parser, "前两季度", None, None, None, None, "前两季度"),
    (nl_parser, "前2季度", None, None, None, None, "前2季度"),
    (nl_parser, "前两个季度", None, None, None, None, "前两季度"),
    (nl_parser, "前2个季度", None, None, None, None, "前2季度"),
    (nl_parser, "两季度前", None, None, None, None, "两季度前"),
    (nl_parser, "2季度前", None, None, None, None, "2季度前"),
    (nl_parser, "两季度内", None, None, None, None, "两季度内"),
    (nl_parser, "2季度内", None, None, None, None, "2季度内"),
    (nl_parser, "两季度以来", None, None, None, None, "两季度以来"),
    (nl_parser, "2季度以来", None, None, None, None, "2季度以来"),
    (nl_parser, "两个季度前", None, None, None, None, "两季度前"),
    (nl_parser, "2个季度前", None, None, None, None, "2季度前"),
    (nl_parser, "两个季度以前", None, None, None, None, "两季度以前"),
    (nl_parser, "2个季度以前", None, None, None, None, "2季度以前"),
    (nl_parser, "两个季度之前", None, None, None, None, "两季度之前"),
    (nl_parser, "2个季度之前", None, None, None, None, "2季度之前"),
    (nl_parser, "两个季度以内", None, None, None, None, "两季度以内"),
    (nl_parser, "2个季度以内", None, None, None, None, "2季度以内"),
    (nl_parser, "两个季度之内", None, None, None, None, "两季度之内"),
    (nl_parser, "2个季度之内", None, None, None, None, "2季度之内"),
    (nl_parser, "两个季度以来", None, None, None, None, "两季度以来"),
    (nl_parser, "2个季度以来", None, None, None, None, "2季度以来"),
]

month_testdata = [
    (nl_parser, "本月", None, None, None, None, "本月"),
    (nl_parser, "本月份", None, None, None, None, "本月"),
    (nl_parser, "本月度", None, None, None, None, "本月"),
    (nl_parser, "这个月", None, None, None, None, "这个月"),
    (nl_parser, "这个月份", None, None, None, None, "这个月"),
    (nl_parser, "当前月", None, None, None, None, "当前月"),
    (nl_parser, "当前月份", None, None, None, None, "当前月"),
    (nl_parser, "上月", None, None, None, None, "上月"),
    (nl_parser, "上月份", None, None, None, None, "上月"),
    (nl_parser, "上个月", None, None, None, None, "上月"),
    (nl_parser, "上个月份", None, None, None, None, "上月"),
    (nl_parser, "下月", None, None, None, None, "下月"),
    (nl_parser, "下月份", None, None, None, None, "下月"),
    (nl_parser, "下个月", None, None, None, None, "下月"),
    (nl_parser, "下个月份", None, None, None, None, "下月"),
    (nl_parser, "两月前", None, None, None, None, "两月前"),
    (nl_parser, "2月前", None, None, None, None, "2月前"),
    (nl_parser, "两月内", None, None, None, None, "两月内"),
    (nl_parser, "2月内", None, None, None, None, "2月内"),
    (nl_parser, "两月以前", None, None, None, None, "两月以前"),
    (nl_parser, "两月之前", None, None, None, None, "两月之前"),
    (nl_parser, "两月以内", None, None, None, None, "两月以内"),
    (nl_parser, "2月以内", None, None, None, None, "2月以内"),
    (nl_parser, "两月之内", None, None, None, None, "两月之内"),
    (nl_parser, "2月之内", None, None, None, None, "2月之内"),
    (nl_parser, "两月以来", None, None, None, None, "两月以来"),
    (nl_parser, "两个月前", None, None, None, None, "两月前"),
    (nl_parser, "2个月前", None, None, None, None, "2月前"),
    (nl_parser, "两个月内", None, None, None, None, "两月内"),
    (nl_parser, "2个月内", None, None, None, None, "2月内"),
    (nl_parser, "两个月以前", None, None, None, None, "两月以前"),
    (nl_parser, "2个月以前", None, None, None, None, "2月以前"),
    (nl_parser, "两个月之前", None, None, None, None, "两月之前"),
    (nl_parser, "2个月之前", None, None, None, None, "2月之前"),
    (nl_parser, "两个月以内", None, None, None, None, "两月以内"),
    (nl_parser, "2个月以内", None, None, None, None, "2月以内"),
    (nl_parser, "两个月之内", None, None, None, None, "两月之内"),
    (nl_parser, "2个月之内", None, None, None, None, "2月之内"),
    (nl_parser, "两个月以来", None, None, None, None, "两月以来"),
    (nl_parser, "2个月以来", None, None, None, None, "2月以来"),
    (nl_parser, "前两月", None, None, None, None, "前两月"),
    (nl_parser, "前2月", None, None, None, None, "前2月"),
    (nl_parser, "前两个月", None, None, None, None, "前两月"),
    (nl_parser, "前2个月", None, None, None, None, "前2月"),
]

week_testdata = [
    (nl_parser, "本周", None, None, None, None, "本周"),
    (nl_parser, "当前周", None, None, None, None, "当前周"),
    (nl_parser, "本星期", None, None, None, None, "本星期"),
    (nl_parser, "这个星期", None, None, None, None, "这个星期"),
    (nl_parser, "当前星期", None, None, None, None, "当前星期"),
    (nl_parser, "上周", None, None, None, None, "上周"),
    (nl_parser, "上星期", None, None, None, None, "上星期"),
    (nl_parser, "上个星期", None, None, None, None, "上星期"),
    (nl_parser, "下周", None, None, None, None, "下周"),
    (nl_parser, "下星期", None, None, None, None, "下星期"),
    (nl_parser, "下个星期", None, None, None, None, "下星期"),
    (nl_parser, "前两星期", None, None, None, None, "前两星期"),
    (nl_parser, "前2星期", None, None, None, None, "前2星期"),
    (nl_parser, "前两个星期", None, None, None, None, "前两星期"),
    (nl_parser, "前2个星期", None, None, None, None, "前2星期"),
    (nl_parser, "两星期前", None, None, None, None, "两星期前"),
    (nl_parser, "2星期前", None, None, None, None, "2星期前"),
    (nl_parser, "两星期内", None, None, None, None, "两星期内"),
    (nl_parser, "2星期内", None, None, None, None, "2星期内"),
    (nl_parser, "两星期以来", None, None, None, None, "两星期以来"),
    (nl_parser, "2星期以来", None, None, None, None, "2星期以来"),
    (nl_parser, "两星期以内", None, None, None, None, "两星期以内"),
    (nl_parser, "2星期以内", None, None, None, None, "2星期以内"),
    (nl_parser, "两星期之内", None, None, None, None, "两星期之内"),
    (nl_parser, "2星期之内", None, None, None, None, "2星期之内"),
    (nl_parser, "两星期以来", None, None, None, None, "两星期以来"),
    (nl_parser, "2星期以来", None, None, None, None, "2星期以来"),
    (nl_parser, "两个星期前", None, None, None, None, "两星期前"),
    (nl_parser, "2个星期前", None, None, None, None, "2星期前"),
    (nl_parser, "两个星期以前", None, None, None, None, "两星期以前"),
    (nl_parser, "2个星期以前", None, None, None, None, "2星期以前"),
    (nl_parser, "两个星期之前", None, None, None, None, "两星期之前"),
    (nl_parser, "2个星期之前", None, None, None, None, "2星期之前"),
    (nl_parser, "两个星期内", None, None, None, None, "两星期内"),
    (nl_parser, "2个星期内", None, None, None, None, "2星期内"),
    (nl_parser, "两个星期以内", None, None, None, None, "两星期以内"),
    (nl_parser, "2个星期以内", None, None, None, None, "2星期以内"),
    (nl_parser, "两个星期之内", None, None, None, None, "两星期之内"),
    (nl_parser, "2个星期之内", None, None, None, None, "2星期之内"),
    (nl_parser, "两个星期以来", None, None, None, None, "两星期以来"),
    (nl_parser, "2个星期以来", None, None, None, None, "2星期以来"),
]

day_testdata = [
    (nl_parser, "今天", None, None, None, None, "今天"),
    (nl_parser, "今日", None, None, None, None, "今日"),
    (nl_parser, "明天", None, None, None, None, "明天"),
    (nl_parser, "明日", None, None, None, None, "明日"),
    (nl_parser, "后天", None, None, None, None, "后天"),
    (nl_parser, "后日", None, None, None, None, "后日"),
    (nl_parser, "昨天", None, None, None, None, "昨天"),
    (nl_parser, "昨日", None, None, None, None, "昨日"),
    (nl_parser, "前天", None, None, None, None, "前天"),
    (nl_parser, "前日", None, None, None, None, "前日"),
    (nl_parser, "上午", None, None, None, None, "上午"),
    (nl_parser, "下午", None, None, None, None, "下午"),
    (nl_parser, "前两天", None, None, None, None, "前两天"),
    (nl_parser, "前2天", None, None, None, None, "前2天"),
    (nl_parser, "前两个天", None, None, None, None, "前两天"),
    (nl_parser, "前2个天", None, None, None, None, "前2天"),
    (nl_parser, "两天前", None, None, None, None, "两天前"),
    (nl_parser, "2天前", None, None, None, None, "2天前"),
    (nl_parser, "两天内", None, None, None, None, "两天内"),
    (nl_parser, "2天内", None, None, None, None, "2天内"),
    (nl_parser, "两天以来", None, None, None, None, "两天以来"),
    (nl_parser, "2天以来", None, None, None, None, "2天以来"),
    (nl_parser, "两天以内", None, None, None, None, "两天以内"),
    (nl_parser, "2天以内", None, None, None, None, "2天以内"),
    (nl_parser, "两天之内", None, None, None, None, "两天之内"),
    (nl_parser, "2天之内", None, None, None, None, "2天之内"),
    (nl_parser, "两天以来", None, None, None, None, "两天以来"),
    (nl_parser, "2天以来", None, None, None, None, "2天以来"),
    (nl_parser, "两个天前", None, None, None, None, "两天前"),
    (nl_parser, "2个天前", None, None, None, None, "2天前"),
    (nl_parser, "两个天以前", None, None, None, None, "两天以前"),
    (nl_parser, "2个天以前", None, None, None, None, "2天以前"),
    (nl_parser, "两个天之前", None, None, None, None, "两天之前"),
    (nl_parser, "2个天之前", None, None, None, None, "2天之前"),
    (nl_parser, "两个天内", None, None, None, None, "两天内"),
    (nl_parser, "2个天内", None, None, None, None, "2天内"),
    (nl_parser, "两个天以内", None, None, None, None, "两天以内"),
    (nl_parser, "2个天以内", None, None, None, None, "2天以内"),
    (nl_parser, "两个天之内", None, None, None, None, "两天之内"),
    (nl_parser, "2个天之内", None, None, None, None, "2天之内"),
    (nl_parser, "两个天以来", None, None, None, None, "两天以来"),
    (nl_parser, "2个天以来", None, None, None, None, "2天以来"),
    (nl_parser, "前两日", None, None, None, None, "前两日"),
    (nl_parser, "前2日", None, None, None, None, "前2日"),
    (nl_parser, "前两个日", None, None, None, None, "前两日"),
    (nl_parser, "前2个日", None, None, None, None, "前2日"),
    (nl_parser, "两日前", None, None, None, None, "两日前"),
    (nl_parser, "2日前", None, None, None, None, "2日前"),
    (nl_parser, "两日内", None, None, None, None, "两日内"),
    (nl_parser, "2日内", None, None, None, None, "2日内"),
    (nl_parser, "两日以来", None, None, None, None, "两日以来"),
    (nl_parser, "两日以内", None, None, None, None, "两日以内"),
    (nl_parser, "2日以内", None, None, None, None, "2日以内"),
    (nl_parser, "两日之内", None, None, None, None, "两日之内"),
    (nl_parser, "2日之内", None, None, None, None, "2日之内"),
    (nl_parser, "两日以来", None, None, None, None, "两日以来"),
    (nl_parser, "两个日前", None, None, None, None, "两日前"),
    (nl_parser, "2个日前", None, None, None, None, "2日前"),
    (nl_parser, "两个日以前", None, None, None, None, "两日以前"),
    (nl_parser, "2个日以前", None, None, None, None, "2日以前"),
    (nl_parser, "两个日之前", None, None, None, None, "两日之前"),
    (nl_parser, "2个日之前", None, None, None, None, "2日之前"),
    (nl_parser, "两个日内", None, None, None, None, "两日内"),
    (nl_parser, "2个日内", None, None, None, None, "2日内"),
    (nl_parser, "两个日以内", None, None, None, None, "两日以内"),
    (nl_parser, "2个日以内", None, None, None, None, "2日以内"),
    (nl_parser, "两个日之内", None, None, None, None, "两日之内"),
    (nl_parser, "2个日之内", None, None, None, None, "2日之内"),
    (nl_parser, "两个日以来", None, None, None, None, "两日以来"),
    (nl_parser, "2个日以来", None, None, None, None, "2日以来"),
]

groupdate_testdata = [
    ("2019年以前", "2019", None, None, "以前", None),
    ("2019年之前", "2019", None, None, "之前", None),
    ("2019年以来", "2019", None, None, "以来", None),
    ("6月以前", None, "6", None, "以前", None),
    ("6月之前", None, "6", None, "之前", None),
    ("6月以来", None, "6", None, "以来", None),
    ("13日以前", None, None, "13", "以前", None),
    ("13日之前", None, None, "13", "之前", None),
    ("13日以来", None, None, "13", "以来", None),
    ("5号以前", None, None, "5", "以前", None),
    ("5号之前", None, None, "5", "之前", None),
    ("5号以来", None, None, "5", "以来", None),
    ("2021年上半年", "2021", None, None, "上半年", None),
    ("2021年第一季度", "2021", None, None, "一季度", None),
    ("2021年9月7日上午", "2021", "9", "7", "上午", None),
]

parse_testdata = [
    *date_testdata,
    # *year_testdata,
    # *quarter_testdata,
    # *month_testdata,
    # *week_testdata,
    # *day_testdata,
    # *groupdate_testdata,
]
