from datetime import datetime
from typing import Tuple

import pytest

from cn2date import parse
from cn2date.util import date_add, date_sub

now = datetime.now()
print("now", now)

now_year = now.year  # 当前日期的年份
now_month = now.month  # 当前日期的月份
now_day = now.day  # 当前日期的天数

date_testdata = [
    # 完整的日期格式
    ("2017-7-23", (datetime(2017, 7, 23), datetime(2017, 7, 24))),
    ("2017/7/23", (datetime(2017, 7, 23), datetime(2017, 7, 24))),
    ("2017年7月23日", (datetime(2017, 7, 23), datetime(2017, 7, 24))),
    ("二零一七年七月二十三", (datetime(2017, 7, 23), datetime(2017, 7, 24))),
    ("二零一七年七月二十三日", (datetime(2017, 7, 23), datetime(2017, 7, 24))),
    # 只包含年的日期格式
    ("17年", (datetime(2017, 1, 1), datetime(2018, 1, 1))),
    ("2017年", (datetime(2017, 1, 1), datetime(2018, 1, 1))),
    ("一七年", (datetime(2017, 1, 1), datetime(2018, 1, 1))),
    ("二零一七年", (datetime(2017, 1, 1), datetime(2018, 1, 1))),
    # 只包含年月的日期格式
    ("17-7", (datetime(2017, 7, 1), datetime(2017, 8, 1))),
    ("17/7", (datetime(2017, 7, 1), datetime(2017, 8, 1))),
    ("17年7月", (datetime(2017, 7, 1), datetime(2017, 8, 1))),
    ("一七年七月", (datetime(2017, 7, 1), datetime(2017, 8, 1))),
    ("2017-7", (datetime(2017, 7, 1), datetime(2017, 8, 1))),
    ("2017/7", (datetime(2017, 7, 1), datetime(2017, 8, 1))),
    ("2017年7月", (datetime(2017, 7, 1), datetime(2017, 8, 1))),
    ("二零一七年七月", (datetime(2017, 7, 1), datetime(2017, 8, 1))),
    # 只包含月的日期格式
    ("7月", (datetime(now_year, 7, 1), datetime(now_year, 8, 1))),
    ("07月", (datetime(now_year, 7, 1), datetime(now_year, 8, 1))),
    ("七月", (datetime(now_year, 7, 1), datetime(now_year, 8, 1))),
    # 只包含月日的日期格式
    # ("07-11", (datetime(now_year, 7, 11), datetime(now_year, 7, 12))), # 优先识别为 年-月
    # ("07/11", (datetime(now_year, 7, 11), datetime(now_year, 7, 12))), # 优先识别为 年/月
    ("07月11", (datetime(now_year, 7, 11), datetime(now_year, 7, 12))),
    ("07月11日", (datetime(now_year, 7, 11), datetime(now_year, 7, 12))),
    ("七月一一日", (datetime(now_year, 7, 11), datetime(now_year, 7, 12))),
    ("七月十一日", (datetime(now_year, 7, 11), datetime(now_year, 7, 12))),
    # 只包含日的日期格式
    ("7日", (datetime(now_year, now_month, 7), datetime(now_year, now_month, 8))),
    ("07日", (datetime(now_year, now_month, 7), datetime(now_year, now_month, 8))),
    ("七日", (datetime(now_year, now_month, 7), datetime(now_year, now_month, 8))),
    ("7号", (datetime(now_year, now_month, 7), datetime(now_year, now_month, 8))),
    ("07号", (datetime(now_year, now_month, 7), datetime(now_year, now_month, 8))),
    ("七号", (datetime(now_year, now_month, 7), datetime(now_year, now_month, 8))),
]


@pytest.mark.parametrize("text,expected", date_testdata, ids=[i[0] for i in date_testdata])
def test_date_parse(text: str, expected: Tuple[datetime, datetime]):
    print("input", text)

    result = parse(text)

    print("output", result)

    assert len(result) == len(expected)

    for i, s in enumerate(expected):
        assert result[i] == s


next_year = date_add(datetime(now_year, 1, 1), 1, "y")  # 明年
the_year_after = date_add(next_year, 1, "y")  # 后年
last_year = date_sub(datetime(now_year, 1, 1), 1, "y")  # 去年
the_year_before = date_sub(last_year, 1, "y")  # 前年

nl_testdata = [
    # 年 口语格式
    ("今年", (datetime(now_year, 1, 1), datetime(now_year + 1, 1, 1))),
    ("本年", (datetime(now_year, 1, 1), datetime(now_year + 1, 1, 1))),
    ("本年份", (datetime(now_year, 1, 1), datetime(now_year + 1, 1, 1))),
    ("本年度", (datetime(now_year, 1, 1), datetime(now_year + 1, 1, 1))),
    ("当前年", (datetime(now_year, 1, 1), datetime(now_year + 1, 1, 1))),
    ("当前年份", (datetime(now_year, 1, 1), datetime(now_year + 1, 1, 1))),
    ("当前年度", (datetime(now_year, 1, 1), datetime(now_year + 1, 1, 1))),
    ("明年", (next_year, the_year_after)),
    ("去年", (last_year, datetime(now_year, 1, 1))),
    ("前年", (the_year_before, last_year)),
    ("上半年", (datetime(now_year, 1, 1), datetime(now_year, 7, 1))),
    ("下半年", (datetime(now_year, 7, 1), datetime(now_year + 1, 1, 1))),
    ("前2年", (the_year_before, datetime(now_year, 1, 1))),
    ("前2个年", (the_year_before, datetime(now_year, 1, 1))),
    ("前2个年份", (the_year_before, datetime(now_year, 1, 1))),
    ("前两年", (the_year_before, datetime(now_year, 1, 1))),
    ("前两个年", (the_year_before, datetime(now_year, 1, 1))),
    ("前两个年份", (the_year_before, datetime(now_year, 1, 1))),
    ("后2年", (next_year, datetime(next_year.year + 2, 1, 1))),
    ("后2个年", (next_year, datetime(next_year.year + 2, 1, 1))),
    ("后2个年份", (next_year, datetime(next_year.year + 2, 1, 1))),
    ("后两年", (next_year, datetime(next_year.year + 2, 1, 1))),
    ("后两个年", (next_year, datetime(next_year.year + 2, 1, 1))),
    ("后两个年份", (next_year, datetime(next_year.year + 2, 1, 1))),
    ("2年前", (the_year_before, last_year)),
    ("两年前", (the_year_before, last_year)),
    ("2年后", (the_year_after, datetime(the_year_after.year + 1, 1, 1))),
    ("两年后", (the_year_after, datetime(the_year_after.year + 1, 1, 1))),
    ("2年内", (last_year, next_year)),
    ("两年内", (last_year, next_year)),
    # # 季度 口语格式
    # ("本季度", (datetime(2021, 7, 1), datetime(2021, 10, 1))),
    # ("这个季度", (datetime(2021, 7, 1), datetime(2021, 10, 1))),
    # ("当前季度", (datetime(2021, 7, 1), datetime(2021, 10, 1))),
    # ("上季度", (datetime(2021, 4, 1), datetime(2021, 7, 1))),
    # ("上个季度", (datetime(2021, 4, 1), datetime(2021, 7, 1))),
    # ("下季度", (datetime(2021, 10, 1), datetime(2022, 1, 1))),
    # ("下个季度", (datetime(2021, 10, 1), datetime(2022, 1, 1))),
    # ("第一季度", (datetime(2021, 1, 1), datetime(2021, 4, 1))),
    # ("第一个季度", (datetime(2021, 1, 1), datetime(2021, 4, 1))),
    # ("第1季度", (datetime(2021, 1, 1), datetime(2021, 4, 1))),
    # ("第1个季度", (datetime(2021, 1, 1), datetime(2021, 4, 1))),
    # ("一季度", (datetime(2021, 1, 1), datetime(2021, 4, 1))),
    # ("1季度", (datetime(2021, 1, 1), datetime(2021, 4, 1))),
    # ("第二季度", (datetime(2021, 4, 1), datetime(2021, 7, 1))),
    # ("第二个季度", (datetime(2021, 4, 1), datetime(2021, 7, 1))),
    # ("第2季度", (datetime(2021, 4, 1), datetime(2021, 7, 1))),
    # ("第2个季度", (datetime(2021, 4, 1), datetime(2021, 7, 1))),
    # ("2季度", (datetime(2021, 4, 1), datetime(2021, 7, 1))),
    # ("二季度", (datetime(2021, 4, 1), datetime(2021, 7, 1))),
    # ("第三季度", (datetime(2021, 7, 1), datetime(2021, 10, 1))),
    # ("第三个季度", (datetime(2021, 7, 1), datetime(2021, 10, 1))),
    # ("第3季度", (datetime(2021, 7, 1), datetime(2021, 10, 1))),
    # ("第3个季度", (datetime(2021, 7, 1), datetime(2021, 10, 1))),
    # ("三季度", (datetime(2021, 7, 1), datetime(2021, 10, 1))),
    # ("3季度", (datetime(2021, 7, 1), datetime(2021, 10, 1))),
    # ("第四季度", (datetime(2021, 10, 1), datetime(2022, 1, 1))),
    # ("第四个季度", (datetime(2021, 10, 1), datetime(2022, 1, 1))),
    # ("第4季度", (datetime(2021, 10, 1), datetime(2022, 1, 1))),
    # ("第4个季度", (datetime(2021, 10, 1), datetime(2022, 1, 1))),
    # ("四季度", (datetime(2021, 10, 1), datetime(2022, 1, 1))),
    # ("4季度", (datetime(2021, 10, 1), datetime(2022, 1, 1))),
    # ("前2季度", (datetime(2021, 1, 1), datetime(2021, 7, 1))),
    # ("前2个季度", (datetime(2021, 1, 1), datetime(2021, 7, 1))),
    # ("前两季度", (datetime(2021, 1, 1), datetime(2021, 7, 1))),
    # ("前两个季度", (datetime(2021, 1, 1), datetime(2021, 7, 1))),
    # ("后2季度", (datetime(2021, 10, 1), datetime(2022, 4, 1))),
    # ("后2个季度", (datetime(2021, 10, 1), datetime(2022, 4, 1))),
    # ("后两季度", (datetime(2021, 10, 1), datetime(2022, 4, 1))),
    # ("后两个季度", (datetime(2021, 10, 1), datetime(2022, 4, 1))),
    # ("2季度前", (datetime(2021, 1, 1), datetime(2021, 4, 1))),
    # ("两季度前", (datetime(2021, 1, 1), datetime(2021, 4, 1))),
    # ("2季度后", (datetime(2022, 1, 1), datetime(2022, 4, 1))),
    # ("两季度后", (datetime(2022, 1, 1), datetime(2022, 4, 1))),
    # ("2季度内", (datetime(2021, 4, 1), datetime(2021, 10, 1))),
    # ("两季度内", (datetime(2021, 4, 1), datetime(2021, 10, 1))),
    # # 月 口语格式
    # ("本月", (datetime(2021, 9, 1), datetime(2021, 10, 1))),
    # ("本月份", (datetime(2021, 9, 1), datetime(2021, 10, 1))),
    # ("本月度", (datetime(2021, 9, 1), datetime(2021, 10, 1))),
    # ("这个月", (datetime(2021, 9, 1), datetime(2021, 10, 1))),
    # ("这个月份", (datetime(2021, 9, 1), datetime(2021, 10, 1))),
    # ("当前月", (datetime(2021, 9, 1), datetime(2021, 10, 1))),
    # ("当前月份", (datetime(2021, 9, 1), datetime(2021, 10, 1))),
    # ("上月", (datetime(2021, 8, 1), datetime(2021, 9, 1))),
    # ("上月份", (datetime(2021, 8, 1), datetime(2021, 9, 1))),
    # ("上个月", (datetime(2021, 8, 1), datetime(2021, 9, 1))),
    # ("上个月份", (datetime(2021, 8, 1), datetime(2021, 9, 1))),
    # ("下月", (datetime(2021, 10, 1), datetime(2021, 11, 1))),
    # ("下月份", (datetime(2021, 10, 1), datetime(2021, 11, 1))),
    # ("下个月", (datetime(2021, 10, 1), datetime(2021, 11, 1))),
    # ("下个月份", (datetime(2021, 10, 1), datetime(2021, 11, 1))),
    # ("前2月", (datetime(2021, 7, 1), datetime(2021, 9, 1))),
    # ("前2个月", (datetime(2021, 7, 1), datetime(2021, 9, 1))),
    # ("前2个月份", (datetime(2021, 7, 1), datetime(2021, 9, 1))),
    # ("前两月", (datetime(2021, 7, 1), datetime(2021, 9, 1))),
    # ("前两个月", (datetime(2021, 7, 1), datetime(2021, 9, 1))),
    # ("前两个月份", (datetime(2021, 7, 1), datetime(2021, 9, 1))),
    # ("后2月", (datetime(2021, 10, 1), datetime(2021, 12, 1))),
    # ("后2个月", (datetime(2021, 10, 1), datetime(2021, 12, 1))),
    # ("后2个月份", (datetime(2021, 10, 1), datetime(2021, 12, 1))),
    # ("后两月", (datetime(2021, 10, 1), datetime(2021, 12, 1))),
    # ("后两个月", (datetime(2021, 10, 1), datetime(2021, 12, 1))),
    # ("后两个月份", (datetime(2021, 10, 1), datetime(2021, 12, 1))),
    # ("2月前", (datetime(2021, 7, 1), datetime(2021, 8, 1))),
    # ("两月前", (datetime(2021, 7, 1), datetime(2021, 8, 1))),
    # ("2月后", (datetime(2021, 11, 1), datetime(2021, 12, 1))),
    # ("两月后", (datetime(2021, 11, 1), datetime(2021, 12, 1))),
    # ("2月内", (datetime(2021, 8, 1), datetime(2021, 10, 1))),
    # ("两月内", (datetime(2021, 8, 1), datetime(2021, 10, 1))),
    # # 周、星期 口语格式
    # ("本周", (datetime(2021, 8, 30), datetime(2021, 9, 6))),
    # ("当前周", (datetime(2021, 8, 30), datetime(2021, 9, 6))),
    # ("上周", (datetime(2021, 8, 23), datetime(2021, 8, 30))),
    # ("下周", (datetime(2021, 9, 6), datetime(2021, 9, 13))),
    # ("前2周", (datetime(2021, 8, 16), datetime(2021, 8, 30))),
    # ("前2个周", (datetime(2021, 8, 16), datetime(2021, 8, 30))),
    # ("前两周", (datetime(2021, 8, 16), datetime(2021, 8, 30))),
    # ("前两个周", (datetime(2021, 8, 16), datetime(2021, 8, 30))),
    # ("后2周", (datetime(2021, 9, 6), datetime(2021, 9, 20))),
    # ("后2个周", (datetime(2021, 9, 6), datetime(2021, 9, 20))),
    # ("后两周", (datetime(2021, 9, 6), datetime(2021, 9, 20))),
    # ("后两个周", (datetime(2021, 9, 6), datetime(2021, 9, 20))),
    # ("2周前", (datetime(2021, 8, 16), datetime(2021, 8, 23))),
    # ("两周前", (datetime(2021, 8, 16), datetime(2021, 8, 23))),
    # ("2周后", (datetime(2021, 9, 13), datetime(2021, 9, 20))),
    # ("两周后", (datetime(2021, 9, 13), datetime(2021, 9, 20))),
    # ("2周内", (datetime(2021, 8, 23), datetime(2021, 9, 6))),
    # ("两周内", (datetime(2021, 8, 23), datetime(2021, 9, 6))),
    # ("本星期", (datetime(2021, 8, 30), datetime(2021, 9, 6))),
    # ("这个星期", (datetime(2021, 8, 30), datetime(2021, 9, 6))),
    # ("当前星期", (datetime(2021, 8, 30), datetime(2021, 9, 6))),
    # ("上星期", (datetime(2021, 8, 23), datetime(2021, 8, 30))),
    # ("上个星期", (datetime(2021, 8, 23), datetime(2021, 8, 30))),
    # ("下星期", (datetime(2021, 9, 6), datetime(2021, 9, 13))),
    # ("下个星期", (datetime(2021, 9, 6), datetime(2021, 9, 13))),
    # ("前2星期", (datetime(2021, 8, 16), datetime(2021, 8, 30))),
    # ("前2个星期", (datetime(2021, 8, 16), datetime(2021, 8, 30))),
    # ("前两星期", (datetime(2021, 8, 16), datetime(2021, 8, 30))),
    # ("前两个星期", (datetime(2021, 8, 16), datetime(2021, 8, 30))),
    # ("后2星期", (datetime(2021, 9, 6), datetime(2021, 9, 20))),
    # ("后2个星期", (datetime(2021, 9, 6), datetime(2021, 9, 20))),
    # ("后两星期", (datetime(2021, 9, 6), datetime(2021, 9, 20))),
    # ("后两个星期", (datetime(2021, 9, 6), datetime(2021, 9, 20))),
    # ("2星期前", (datetime(2021, 8, 16), datetime(2021, 8, 23))),
    # ("两星期前", (datetime(2021, 8, 16), datetime(2021, 8, 23))),
    # ("2星期后", (datetime(2021, 9, 13), datetime(2021, 9, 20))),
    # ("两星期后", (datetime(2021, 9, 13), datetime(2021, 9, 20))),
    # ("2星期内", (datetime(2021, 8, 23), datetime(2021, 9, 6))),
    # ("两星期内", (datetime(2021, 8, 23), datetime(2021, 9, 6))),
    # # 日、天 口语格式
    # ("今天", (datetime(2021, 9, 1), datetime(2021, 9, 2))),
    # ("上午", (datetime(2021, 9, 1), datetime(2021, 9, 1, 12))),
    # ("下午", (datetime(2021, 9, 1, 12), datetime(2021, 9, 1, 19))),
    # ("今日", (datetime(2021, 9, 1), datetime(2021, 9, 2))),
    # ("明日", (datetime(2021, 9, 2), datetime(2021, 9, 3))),
    # ("后日", (datetime(2021, 9, 3), datetime(2021, 9, 4))),
    # ("昨日", (datetime(2021, 8, 31), datetime(2021, 9, 1))),
    # ("前日", (datetime(2021, 8, 30), datetime(2021, 8, 31))),
    # ("前2日", (datetime(2021, 8, 30), datetime(2021, 9, 1))),
    # ("前2个日", (datetime(2021, 8, 30), datetime(2021, 9, 1))),
    # ("前两日", (datetime(2021, 8, 30), datetime(2021, 9, 1))),
    # ("前两个日", (datetime(2021, 8, 30), datetime(2021, 9, 1))),
    # ("后2日", (datetime(2021, 9, 2), datetime(2021, 9, 4))),
    # ("后2个日", (datetime(2021, 9, 2), datetime(2021, 9, 4))),
    # ("后两日", (datetime(2021, 9, 2), datetime(2021, 9, 4))),
    # ("后两个日", (datetime(2021, 9, 2), datetime(2021, 9, 4))),
    # ("2日前", (datetime(2021, 8, 30), datetime(2021, 8, 31))),
    # ("两日前", (datetime(2021, 8, 30), datetime(2021, 8, 31))),
    # ("2日后", (datetime(2021, 9, 3), datetime(2021, 9, 4))),
    # ("两日后", (datetime(2021, 9, 3), datetime(2021, 9, 4))),
    # ("2日内", (datetime(2021, 8, 31), datetime(2021, 9, 2))),
    # ("两日内", (datetime(2021, 8, 31), datetime(2021, 9, 2))),
    # ("明天", (datetime(2021, 9, 2), datetime(2021, 9, 3))),
    # ("后天", (datetime(2021, 9, 3), datetime(2021, 9, 4))),
    # ("昨天", (datetime(2021, 8, 31), datetime(2021, 9, 1))),
    # ("前天", (datetime(2021, 8, 30), datetime(2021, 8, 31))),
    # ("前2天", (datetime(2021, 8, 30), datetime(2021, 9, 1))),
    # ("前2个天", (datetime(2021, 8, 30), datetime(2021, 9, 1))),
    # ("前两天", (datetime(2021, 8, 30), datetime(2021, 9, 1))),
    # ("前两个天", (datetime(2021, 8, 30), datetime(2021, 9, 1))),
    # ("后2天", (datetime(2021, 9, 2), datetime(2021, 9, 4))),
    # ("后2个天", (datetime(2021, 9, 2), datetime(2021, 9, 4))),
    # ("后两天", (datetime(2021, 9, 2), datetime(2021, 9, 4))),
    # ("后两个天", (datetime(2021, 9, 2), datetime(2021, 9, 4))),
    # ("2天前", (datetime(2021, 8, 30), datetime(2021, 8, 31))),
    # ("两天前", (datetime(2021, 8, 30), datetime(2021, 8, 31))),
    # ("2天后", (datetime(2021, 9, 3), datetime(2021, 9, 4))),
    # ("两天后", (datetime(2021, 9, 3), datetime(2021, 9, 4))),
    # ("2天内", (datetime(2021, 8, 31), datetime(2021, 9, 2))),
    # ("两天内", (datetime(2021, 8, 31), datetime(2021, 9, 2))),
]


@pytest.mark.parametrize("text,expected", nl_testdata, ids=[i[0] for i in nl_testdata])
def test_nl_parse(text: str, expected: Tuple[datetime, datetime]):
    print("input", text)

    result = parse(text)

    print("output", result)

    assert len(result) == len(expected)

    for i, s in enumerate(expected):
        assert result[i] == s


group_testdata = [
    ("2019年以前", (datetime.min, datetime(2019, 1, 1))),
    ("19年以前", (datetime.min, datetime(2019, 1, 1))),
    ("二零一九年以前", (datetime.min, datetime(2019, 1, 1))),
    ("一九年以前", (datetime.min, datetime(2019, 1, 1))),
    ("2019年以后", (datetime(2020, 1, 1), datetime.max)),
    ("19年以后", (datetime(2020, 1, 1), datetime.max)),
    ("二零一九年以后", (datetime(2020, 1, 1), datetime.max)),
    ("一九年以后", (datetime(2020, 1, 1), datetime.max)),
    ("2019年以来", (datetime(2019, 1, 1), datetime(2021, 9, 2))),
    ("19年以来", (datetime(2019, 1, 1), datetime(2021, 9, 2))),
    ("二零一九年以来", (datetime(2019, 1, 1), datetime(2021, 9, 2))),
    ("一九年以来", (datetime(2019, 1, 1), datetime(2021, 9, 2))),
    ("2017年上半年", (datetime(2017, 1, 1), datetime(2017, 7, 1))),
    ("17年上半年", (datetime(2017, 1, 1), datetime(2017, 7, 1))),
    ("二零一七年上半年", (datetime(2017, 1, 1), datetime(2017, 7, 1))),
    ("一七年上半年", (datetime(2017, 1, 1), datetime(2017, 7, 1))),
    ("2017年下半年", (datetime(2017, 7, 1), datetime(2018, 1, 1))),
    ("17年下半年", (datetime(2017, 7, 1), datetime(2018, 1, 1))),
    ("二零一七年下半年", (datetime(2017, 7, 1), datetime(2018, 1, 1))),
    ("一七年下半年", (datetime(2017, 7, 1), datetime(2018, 1, 1))),
    ("2019年第一季度", (datetime(2019, 1, 1), datetime(2019, 4, 1))),
    ("2019年第一个季度", (datetime(2019, 1, 1), datetime(2019, 4, 1))),
    ("2019年一季度", (datetime(2019, 1, 1), datetime(2019, 4, 1))),
    ("2019年第1季度", (datetime(2019, 1, 1), datetime(2019, 4, 1))),
    ("2019年第1个季度", (datetime(2019, 1, 1), datetime(2019, 4, 1))),
    ("2019年1季度", (datetime(2019, 1, 1), datetime(2019, 4, 1))),
    ("19年第一季度", (datetime(2019, 1, 1), datetime(2019, 4, 1))),
    ("19年第一个季度", (datetime(2019, 1, 1), datetime(2019, 4, 1))),
    ("19年一季度", (datetime(2019, 1, 1), datetime(2019, 4, 1))),
    ("19年第1季度", (datetime(2019, 1, 1), datetime(2019, 4, 1))),
    ("19年第1个季度", (datetime(2019, 1, 1), datetime(2019, 4, 1))),
    ("19年1季度", (datetime(2019, 1, 1), datetime(2019, 4, 1))),
    ("二零一九年第一季度", (datetime(2019, 1, 1), datetime(2019, 4, 1))),
    ("二零一九年第一个季度", (datetime(2019, 1, 1), datetime(2019, 4, 1))),
    ("二零一九年一季度", (datetime(2019, 1, 1), datetime(2019, 4, 1))),
    ("二零一九年第1季度", (datetime(2019, 1, 1), datetime(2019, 4, 1))),
    ("二零一九年第1个季度", (datetime(2019, 1, 1), datetime(2019, 4, 1))),
    ("二零一九年1季度", (datetime(2019, 1, 1), datetime(2019, 4, 1))),
    ("一九年第一季度", (datetime(2019, 1, 1), datetime(2019, 4, 1))),
    ("一九年第一个季度", (datetime(2019, 1, 1), datetime(2019, 4, 1))),
    ("一九年一季度", (datetime(2019, 1, 1), datetime(2019, 4, 1))),
    ("一九年第1季度", (datetime(2019, 1, 1), datetime(2019, 4, 1))),
    ("一九年第1个季度", (datetime(2019, 1, 1), datetime(2019, 4, 1))),
    ("一九年1季度", (datetime(2019, 1, 1), datetime(2019, 4, 1))),
    ("2019年第二季度", (datetime(2019, 4, 1), datetime(2019, 7, 1))),
    ("2019年第二个季度", (datetime(2019, 4, 1), datetime(2019, 7, 1))),
    ("2019年二季度", (datetime(2019, 4, 1), datetime(2019, 7, 1))),
    ("2019年第2季度", (datetime(2019, 4, 1), datetime(2019, 7, 1))),
    ("2019年第2个季度", (datetime(2019, 4, 1), datetime(2019, 7, 1))),
    ("2019年2季度", (datetime(2019, 4, 1), datetime(2019, 7, 1))),
    ("19年第二季度", (datetime(2019, 4, 1), datetime(2019, 7, 1))),
    ("19年第二个季度", (datetime(2019, 4, 1), datetime(2019, 7, 1))),
    ("19年二季度", (datetime(2019, 4, 1), datetime(2019, 7, 1))),
    ("19年第2季度", (datetime(2019, 4, 1), datetime(2019, 7, 1))),
    ("19年第2个季度", (datetime(2019, 4, 1), datetime(2019, 7, 1))),
    ("19年2季度", (datetime(2019, 4, 1), datetime(2019, 7, 1))),
    ("二零一九年第二季度", (datetime(2019, 4, 1), datetime(2019, 7, 1))),
    ("二零一九年第二个季度", (datetime(2019, 4, 1), datetime(2019, 7, 1))),
    ("二零一九年二季度", (datetime(2019, 4, 1), datetime(2019, 7, 1))),
    ("二零一九年第2季度", (datetime(2019, 4, 1), datetime(2019, 7, 1))),
    ("二零一九年第2个季度", (datetime(2019, 4, 1), datetime(2019, 7, 1))),
    ("二零一九年2季度", (datetime(2019, 4, 1), datetime(2019, 7, 1))),
    ("一九年第二季度", (datetime(2019, 4, 1), datetime(2019, 7, 1))),
    ("一九年第二个季度", (datetime(2019, 4, 1), datetime(2019, 7, 1))),
    ("一九年二季度", (datetime(2019, 4, 1), datetime(2019, 7, 1))),
    ("一九年第2季度", (datetime(2019, 4, 1), datetime(2019, 7, 1))),
    ("一九年第2个季度", (datetime(2019, 4, 1), datetime(2019, 7, 1))),
    ("一九年2季度", (datetime(2019, 4, 1), datetime(2019, 7, 1))),
    ("2019年第三季度", (datetime(2019, 7, 1), datetime(2019, 10, 1))),
    ("2019年第三个季度", (datetime(2019, 7, 1), datetime(2019, 10, 1))),
    ("2019年三季度", (datetime(2019, 7, 1), datetime(2019, 10, 1))),
    ("2019年第3季度", (datetime(2019, 7, 1), datetime(2019, 10, 1))),
    ("2019年第3个季度", (datetime(2019, 7, 1), datetime(2019, 10, 1))),
    ("2019年3季度", (datetime(2019, 7, 1), datetime(2019, 10, 1))),
    ("19年第三季度", (datetime(2019, 7, 1), datetime(2019, 10, 1))),
    ("19年第三个季度", (datetime(2019, 7, 1), datetime(2019, 10, 1))),
    ("19年三季度", (datetime(2019, 7, 1), datetime(2019, 10, 1))),
    ("19年第3季度", (datetime(2019, 7, 1), datetime(2019, 10, 1))),
    ("19年第3个季度", (datetime(2019, 7, 1), datetime(2019, 10, 1))),
    ("19年3季度", (datetime(2019, 7, 1), datetime(2019, 10, 1))),
    ("二零一九年第三季度", (datetime(2019, 7, 1), datetime(2019, 10, 1))),
    ("二零一九年第三个季度", (datetime(2019, 7, 1), datetime(2019, 10, 1))),
    ("二零一九年三季度", (datetime(2019, 7, 1), datetime(2019, 10, 1))),
    ("二零一九年第3季度", (datetime(2019, 7, 1), datetime(2019, 10, 1))),
    ("二零一九年第3个季度", (datetime(2019, 7, 1), datetime(2019, 10, 1))),
    ("二零一九年3季度", (datetime(2019, 7, 1), datetime(2019, 10, 1))),
    ("一九年第三季度", (datetime(2019, 7, 1), datetime(2019, 10, 1))),
    ("一九年第三个季度", (datetime(2019, 7, 1), datetime(2019, 10, 1))),
    ("一九年三季度", (datetime(2019, 7, 1), datetime(2019, 10, 1))),
    ("一九年第3季度", (datetime(2019, 7, 1), datetime(2019, 10, 1))),
    ("一九年第3个季度", (datetime(2019, 7, 1), datetime(2019, 10, 1))),
    ("一九年3季度", (datetime(2019, 7, 1), datetime(2019, 10, 1))),
    ("2019年第四季度", (datetime(2019, 10, 1), datetime(2020, 1, 1))),
    ("2019年第四个季度", (datetime(2019, 10, 1), datetime(2020, 1, 1))),
    ("2019年四季度", (datetime(2019, 10, 1), datetime(2020, 1, 1))),
    ("2019年第4季度", (datetime(2019, 10, 1), datetime(2020, 1, 1))),
    ("2019年第4个季度", (datetime(2019, 10, 1), datetime(2020, 1, 1))),
    ("2019年4季度", (datetime(2019, 10, 1), datetime(2020, 1, 1))),
    ("19年第四季度", (datetime(2019, 10, 1), datetime(2020, 1, 1))),
    ("19年第四个季度", (datetime(2019, 10, 1), datetime(2020, 1, 1))),
    ("19年四季度", (datetime(2019, 10, 1), datetime(2020, 1, 1))),
    ("19年第4季度", (datetime(2019, 10, 1), datetime(2020, 1, 1))),
    ("19年第4个季度", (datetime(2019, 10, 1), datetime(2020, 1, 1))),
    ("19年4季度", (datetime(2019, 10, 1), datetime(2020, 1, 1))),
    ("二零一九年第四季度", (datetime(2019, 10, 1), datetime(2020, 1, 1))),
    ("二零一九年第四个季度", (datetime(2019, 10, 1), datetime(2020, 1, 1))),
    ("二零一九年四季度", (datetime(2019, 10, 1), datetime(2020, 1, 1))),
    ("二零一九年第4季度", (datetime(2019, 10, 1), datetime(2020, 1, 1))),
    ("二零一九年第4个季度", (datetime(2019, 10, 1), datetime(2020, 1, 1))),
    ("二零一九年4季度", (datetime(2019, 10, 1), datetime(2020, 1, 1))),
    ("一九年第四季度", (datetime(2019, 10, 1), datetime(2020, 1, 1))),
    ("一九年第四个季度", (datetime(2019, 10, 1), datetime(2020, 1, 1))),
    ("一九年四季度", (datetime(2019, 10, 1), datetime(2020, 1, 1))),
    ("一九年第4季度", (datetime(2019, 10, 1), datetime(2020, 1, 1))),
    ("一九年第4个季度", (datetime(2019, 10, 1), datetime(2020, 1, 1))),
    ("一九年4季度", (datetime(2019, 10, 1), datetime(2020, 1, 1))),
]
