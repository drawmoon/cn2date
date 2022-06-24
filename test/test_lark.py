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


def __simple_transform(n: str, cast_chart_ten=False) -> str:
    _0 = "零"
    _1 = "一"
    _10 = "十"
    t = {
        "0": _0,
        "1": _1,
        "2": "二",
        "3": "三",
        "4": "四",
        "5": "五",
        "6": "六",
        "7": "七",
        "8": "八",
        "9": "九",
    }

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
    unmatched = [
        "0",
        "32",
        "011",
        "111",
        "零",
        "三二",
        "三十二",
        "零十",
        "十零",
        "十十",
        "一十",
        "一十一",
        "一一一",
    ]

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


nl_testdata = [
    # 年
    ("今年", "今年"),
    ("本年", "本年"),
    ("本年份", "本年"),
    ("本年度", "本年"),
    ("当前年", "当前年"),
    ("当前年份", "当前年"),
    ("当前年度", "当前年"),
    ("明年", "明年"),
    ("去年", "去年"),
    ("前年", "前年"),
    ("上半年", "上半年"),
    ("下半年", "下半年"),
    ("前两年", "前两年"),
    ("前2年", "前2年"),
    ("前两个年", "前两年"),
    ("前2个年", "前2年"),
    ("前两个年份", "前两年"),
    ("前2个年份", "前2年"),
    ("两年前", "两年前"),
    ("2年前", "2年前"),
    ("两年内", "两年内"),
    ("2年内", "2年内"),
    ("两年以前", "两年以前"),
    ("2年以前", "2年以前"),
    ("两年之前", "两年之前"),
    ("2年之前", "2年之前"),
    ("两年以内", "两年以内"),
    ("2年以内", "2年以内"),
    ("两年之内", "两年之内"),
    ("2年之内", "2年之内"),
    ("两年以来", "两年以来"),
    ("2年以来", "2年以来"),
    # 季度
    ("本季度", "本季度"),
    ("这个季度", "这个季度"),
    ("当前季度", "当前季度"),
    ("上季度", "上季度"),
    ("上个季度", "上季度"),
    ("下季度", "下季度"),
    ("下个季度", "下季度"),
    ("第一季度", "一季度"),
    ("第一个季度", "一季度"),
    ("第1季度", "1季度"),
    ("第1个季度", "1季度"),
    ("一季度", "一季度"),
    ("1季度", "1季度"),
    ("第二季度", "二季度"),
    ("第二个季度", "二季度"),
    ("第2季度", "2季度"),
    ("第2个季度", "2季度"),
    ("2季度", "2季度"),
    ("二季度", "二季度"),
    ("第三季度", "三季度"),
    ("第三个季度", "三季度"),
    ("第3季度", "3季度"),
    ("第3个季度", "3季度"),
    ("三季度", "三季度"),
    ("3季度", "3季度"),
    ("第四季度", "四季度"),
    ("第四个季度", "四季度"),
    ("第4季度", "4季度"),
    ("第4个季度", "4季度"),
    ("四季度", "四季度"),
    ("4季度", "4季度"),
    ("前两季度", "前两季度"),
    ("前2季度", "前2季度"),
    ("前两个季度", "前两季度"),
    ("前2个季度", "前2季度"),
    ("两季度前", "两季度前"),
    ("2季度前", "2季度前"),
    ("两季度内", "两季度内"),
    ("2季度内", "2季度内"),
    ("两季度以来", "两季度以来"),
    ("2季度以来", "2季度以来"),
    ("两个季度前", "两季度前"),
    ("2个季度前", "2季度前"),
    ("两个季度以前", "两季度以前"),
    ("2个季度以前", "2季度以前"),
    ("两个季度之前", "两季度之前"),
    ("2个季度之前", "2季度之前"),
    ("两个季度以内", "两季度以内"),
    ("2个季度以内", "2季度以内"),
    ("两个季度之内", "两季度之内"),
    ("2个季度之内", "2季度之内"),
    ("两个季度以来", "两季度以来"),
    ("2个季度以来", "2季度以来"),
    # 月
    ("本月", "本月"),
    ("本月份", "本月"),
    ("本月度", "本月"),
    ("这个月", "这个月"),
    ("这个月份", "这个月"),
    ("当前月", "当前月"),
    ("当前月份", "当前月"),
    ("上月", "上月"),
    ("上月份", "上月"),
    ("上个月", "上月"),
    ("上个月份", "上月"),
    ("下月", "下月"),
    ("下月份", "下月"),
    ("下个月", "下月"),
    ("下个月份", "下月"),
    ("两月前", "两月前"),
    ("2月前", "2月前"),
    ("两月内", "两月内"),
    ("2月内", "2月内"),
    ("两月以前", "两月以前"),
    ("两月之前", "两月之前"),
    ("两月以内", "两月以内"),
    ("2月以内", "2月以内"),
    ("两月之内", "两月之内"),
    ("2月之内", "2月之内"),
    ("两月以来", "两月以来"),
    ("两个月前", "两月前"),
    ("2个月前", "2月前"),
    ("两个月内", "两月内"),
    ("2个月内", "2月内"),
    ("两个月以前", "两月以前"),
    ("2个月以前", "2月以前"),
    ("两个月之前", "两月之前"),
    ("2个月之前", "2月之前"),
    ("两个月以内", "两月以内"),
    ("2个月以内", "2月以内"),
    ("两个月之内", "两月之内"),
    ("2个月之内", "2月之内"),
    ("两个月以来", "两月以来"),
    ("2个月以来", "2月以来"),
    ("前两月", "前两月"),
    ("前2月", "前2月"),
    ("前两个月", "前两月"),
    ("前2个月", "前2月"),
    # 周
    ("本周", "本周"),
    ("当前周", "当前周"),
    ("本星期", "本星期"),
    ("这个星期", "这个星期"),
    ("当前星期", "当前星期"),
    ("上周", "上周"),
    ("上星期", "上星期"),
    ("上个星期", "上星期"),
    ("下周", "下周"),
    ("下星期", "下星期"),
    ("下个星期", "下星期"),
    ("前两星期", "前两星期"),
    ("前2星期", "前2星期"),
    ("前两个星期", "前两星期"),
    ("前2个星期", "前2星期"),
    ("两星期前", "两星期前"),
    ("2星期前", "2星期前"),
    ("两星期内", "两星期内"),
    ("2星期内", "2星期内"),
    ("两星期以来", "两星期以来"),
    ("2星期以来", "2星期以来"),
    ("两星期以内", "两星期以内"),
    ("2星期以内", "2星期以内"),
    ("两星期之内", "两星期之内"),
    ("2星期之内", "2星期之内"),
    ("两星期以来", "两星期以来"),
    ("2星期以来", "2星期以来"),
    ("两个星期前", "两星期前"),
    ("2个星期前", "2星期前"),
    ("两个星期以前", "两星期以前"),
    ("2个星期以前", "2星期以前"),
    ("两个星期之前", "两星期之前"),
    ("2个星期之前", "2星期之前"),
    ("两个星期内", "两星期内"),
    ("2个星期内", "2星期内"),
    ("两个星期以内", "两星期以内"),
    ("2个星期以内", "2星期以内"),
    ("两个星期之内", "两星期之内"),
    ("2个星期之内", "2星期之内"),
    ("两个星期以来", "两星期以来"),
    ("2个星期以来", "2星期以来"),
    # 天
    ("今天", "今天"),
    ("今日", "今日"),
    ("明天", "明天"),
    ("明日", "明日"),
    ("后天", "后天"),
    ("后日", "后日"),
    ("昨天", "昨天"),
    ("昨日", "昨日"),
    ("前天", "前天"),
    ("前日", "前日"),
    ("上午", "上午"),
    ("下午", "下午"),
    ("前两天", "前两天"),
    ("前2天", "前2天"),
    ("前两个天", "前两天"),
    ("前2个天", "前2天"),
    ("两天前", "两天前"),
    ("2天前", "2天前"),
    ("两天内", "两天内"),
    ("2天内", "2天内"),
    ("两天以来", "两天以来"),
    ("2天以来", "2天以来"),
    ("两天以内", "两天以内"),
    ("2天以内", "2天以内"),
    ("两天之内", "两天之内"),
    ("2天之内", "2天之内"),
    ("两天以来", "两天以来"),
    ("2天以来", "2天以来"),
    ("两个天前", "两天前"),
    ("2个天前", "2天前"),
    ("两个天以前", "两天以前"),
    ("2个天以前", "2天以前"),
    ("两个天之前", "两天之前"),
    ("2个天之前", "2天之前"),
    ("两个天内", "两天内"),
    ("2个天内", "2天内"),
    ("两个天以内", "两天以内"),
    ("2个天以内", "2天以内"),
    ("两个天之内", "两天之内"),
    ("2个天之内", "2天之内"),
    ("两个天以来", "两天以来"),
    ("2个天以来", "2天以来"),
    ("前两日", "前两日"),
    ("前2日", "前2日"),
    ("前两个日", "前两日"),
    ("前2个日", "前2日"),
    ("两日前", "两日前"),
    ("2日前", "2日前"),
    ("两日内", "两日内"),
    ("2日内", "2日内"),
    ("两日以来", "两日以来"),
    ("两日以内", "两日以内"),
    ("2日以内", "2日以内"),
    ("两日之内", "两日之内"),
    ("2日之内", "2日之内"),
    ("两日以来", "两日以来"),
    ("两个日前", "两日前"),
    ("2个日前", "2日前"),
    ("两个日以前", "两日以前"),
    ("2个日以前", "2日以前"),
    ("两个日之前", "两日之前"),
    ("2个日之前", "2日之前"),
    ("两个日内", "两日内"),
    ("2个日内", "2日内"),
    ("两个日以内", "两日以内"),
    ("2个日以内", "2日以内"),
    ("两个日之内", "两日之内"),
    ("2个日之内", "2日之内"),
    ("两个日以来", "两日以来"),
    ("2个日以来", "2日以来"),
]

group_testdata = [
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
