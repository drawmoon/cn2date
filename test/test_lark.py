from pathlib import Path
from typing import Union

import pytest
from lark import Lark, Tree, Visitor

from cn2date.visitors import scan_value

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
    ("21年09月", "21", "09", None),
    ("21年9月", "21", "9", None),
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


class DateTreeVisitorForTest(Visitor):
    def __init__(self):
        self.years_str: Union[str, None] = None
        self.months_str: Union[str, None] = None
        self.days_str: Union[str, None] = None

    def years(self, tree: Tree):
        self.years_str = scan_value(tree)

    def months(self, tree: Tree):
        self.months_str = scan_value(tree)

    def days(self, tree: Tree):
        self.days_str = scan_value(tree)


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
    tree = date_parser.parse(text)

    visitor = DateTreeVisitorForTest()
    visitor.visit(tree)

    assert visitor.years_str == expected_years
    assert visitor.months_str == expected_months
    assert visitor.days_str == expected_days


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
