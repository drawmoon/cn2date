import unittest
from datetime import datetime

from freezegun import freeze_time

from .cn2date import parse


@freeze_time("2021-9-1 11:23:45")
class Cn2DateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.norm_data_dict = {
            # 完整的日期格式
            "2017-7-23": (
                datetime(2017, 7, 23),
                datetime(2017, 7, 23, 23, 59, 59, 999999),
            ),
            "2017/7/23": (
                datetime(2017, 7, 23),
                datetime(2017, 7, 23, 23, 59, 59, 999999),
            ),
            "2017年7月23日": (
                datetime(2017, 7, 23),
                datetime(2017, 7, 23, 23, 59, 59, 999999),
            ),
            "二零一七年七月二十三": (
                datetime(2017, 7, 23),
                datetime(2017, 7, 23, 23, 59, 59, 999999),
            ),
            "二零一七年七月二十三日": (
                datetime(2017, 7, 23),
                datetime(2017, 7, 23, 23, 59, 59, 999999),
            ),
            # 只包含年的日期格式
            "17年": (datetime(2017, 1, 1), datetime(2017, 12, 31, 23, 59, 59, 999999)),
            "2017年": (datetime(2017, 1, 1), datetime(2017, 12, 31, 23, 59, 59, 999999)),
            "一七年": (datetime(2017, 1, 1), datetime(2017, 12, 31, 23, 59, 59, 999999)),
            "二零一七年": (datetime(2017, 1, 1), datetime(2017, 12, 31, 23, 59, 59, 999999)),
            # 只包含年月的日期格式
            "17-7": (datetime(2017, 7, 1), datetime(2017, 7, 31, 23, 59, 59, 999999)),
            "17/7": (datetime(2017, 7, 1), datetime(2017, 7, 31, 23, 59, 59, 999999)),
            "17年7月": (datetime(2017, 7, 1), datetime(2017, 7, 31, 23, 59, 59, 999999)),
            "一七年七月": (datetime(2017, 7, 1), datetime(2017, 7, 31, 23, 59, 59, 999999)),
            "2017-7": (datetime(2017, 7, 1), datetime(2017, 7, 31, 23, 59, 59, 999999)),
            "2017/7": (datetime(2017, 7, 1), datetime(2017, 7, 31, 23, 59, 59, 999999)),
            "2017年7月": (datetime(2017, 7, 1), datetime(2017, 7, 31, 23, 59, 59, 999999)),
            "二零一七年七月": (datetime(2017, 7, 1), datetime(2017, 7, 31, 23, 59, 59, 999999)),
            # 只包含月的日期格式
            "7月": (datetime(2021, 7, 1), datetime(2021, 7, 31, 23, 59, 59, 999999)),
            "07月": (datetime(2021, 7, 1), datetime(2021, 7, 31, 23, 59, 59, 999999)),
            "七月": (datetime(2021, 7, 1), datetime(2021, 7, 31, 23, 59, 59, 999999)),
            # 只包含月日的日期格式
            # "07-11": (datetime(2021, 7, 11), datetime(2021, 7, 11, 23, 59, 59, 999999)), # 优先识别为 年-月
            # "07/11": (datetime(2021, 7, 11), datetime(2021, 7, 11, 23, 59, 59, 999999)), # 优先识别为 年/月
            "07月11": (datetime(2021, 7, 11), datetime(2021, 7, 11, 23, 59, 59, 999999)),
            "07月11日": (datetime(2021, 7, 11), datetime(2021, 7, 11, 23, 59, 59, 999999)),
            "七月一一日": (datetime(2021, 7, 11), datetime(2021, 7, 11, 23, 59, 59, 999999)),
            "七月十一日": (datetime(2021, 7, 11), datetime(2021, 7, 11, 23, 59, 59, 999999)),
            # 只包含日的日期格式
            "7日": (datetime(2021, 9, 7), datetime(2021, 9, 7, 23, 59, 59, 999999)),
            "07日": (datetime(2021, 9, 7), datetime(2021, 9, 7, 23, 59, 59, 999999)),
            "七日": (datetime(2021, 9, 7), datetime(2021, 9, 7, 23, 59, 59, 999999)),
            "7号": (datetime(2021, 9, 7), datetime(2021, 9, 7, 23, 59, 59, 999999)),
            "07号": (datetime(2021, 9, 7), datetime(2021, 9, 7, 23, 59, 59, 999999)),
            "七号": (datetime(2021, 9, 7), datetime(2021, 9, 7, 23, 59, 59, 999999)),
        }
        self.cn_data_dict = {
            # 年 口语格式
            "今年": (datetime(2021, 1, 1), datetime(2021, 12, 31, 23, 59, 59, 999999)),
            "本年": (datetime(2021, 1, 1), datetime(2021, 12, 31, 23, 59, 59, 999999)),
            "本年份": (datetime(2021, 1, 1), datetime(2021, 12, 31, 23, 59, 59, 999999)),
            "本年度": (datetime(2021, 1, 1), datetime(2021, 12, 31, 23, 59, 59, 999999)),
            "当前年": (datetime(2021, 1, 1), datetime(2021, 12, 31, 23, 59, 59, 999999)),
            "当前年份": (datetime(2021, 1, 1), datetime(2021, 12, 31, 23, 59, 59, 999999)),
            "当前年度": (datetime(2021, 1, 1), datetime(2021, 12, 31, 23, 59, 59, 999999)),
            "明年": (datetime(2022, 1, 1), datetime(2022, 12, 31, 23, 59, 59, 999999)),
            "去年": (datetime(2020, 1, 1), datetime(2020, 12, 31, 23, 59, 59, 999999)),
            "前年": (datetime(2019, 1, 1), datetime(2019, 12, 31, 23, 59, 59, 999999)),
            "上半年": (datetime(2021, 1, 1), datetime(2021, 6, 30, 23, 59, 59, 999999)),
            "下半年": (datetime(2021, 7, 1), datetime(2021, 12, 31, 23, 59, 59, 999999)),
            "前2年": (datetime(2019, 1, 1), datetime(2020, 12, 31, 23, 59, 59, 999999)),
            "前2个年": (datetime(2019, 1, 1), datetime(2020, 12, 31, 23, 59, 59, 999999)),
            "前2个年份": (datetime(2019, 1, 1), datetime(2020, 12, 31, 23, 59, 59, 999999)),
            "前两年": (datetime(2019, 1, 1), datetime(2020, 12, 31, 23, 59, 59, 999999)),
            "前两个年": (datetime(2019, 1, 1), datetime(2020, 12, 31, 23, 59, 59, 999999)),
            "前两个年份": (datetime(2019, 1, 1), datetime(2020, 12, 31, 23, 59, 59, 999999)),
            "后2年": (datetime(2022, 1, 1), datetime(2023, 12, 31, 23, 59, 59, 999999)),
            "后2个年": (datetime(2022, 1, 1), datetime(2023, 12, 31, 23, 59, 59, 999999)),
            "后2个年份": (datetime(2022, 1, 1), datetime(2023, 12, 31, 23, 59, 59, 999999)),
            "后两年": (datetime(2022, 1, 1), datetime(2023, 12, 31, 23, 59, 59, 999999)),
            "后两个年": (datetime(2022, 1, 1), datetime(2023, 12, 31, 23, 59, 59, 999999)),
            "后两个年份": (datetime(2022, 1, 1), datetime(2023, 12, 31, 23, 59, 59, 999999)),
            "2年前": (datetime(2019, 1, 1), datetime(2019, 12, 31, 23, 59, 59, 999999)),
            "两年前": (datetime(2019, 1, 1), datetime(2019, 12, 31, 23, 59, 59, 999999)),
            "2年后": (datetime(2023, 1, 1), datetime(2023, 12, 31, 23, 59, 59, 999999)),
            "两年后": (datetime(2023, 1, 1), datetime(2023, 12, 31, 23, 59, 59, 999999)),
            "2年内": (datetime(2020, 1, 1), datetime(2021, 12, 31, 23, 59, 59, 999999)),
            "两年内": (datetime(2020, 1, 1), datetime(2021, 12, 31, 23, 59, 59, 999999)),
            # 季度 口语格式
            "本季度": (datetime(2021, 7, 1), datetime(2021, 9, 30, 23, 59, 59, 999999)),
            "这个季度": (datetime(2021, 7, 1), datetime(2021, 9, 30, 23, 59, 59, 999999)),
            "当前季度": (datetime(2021, 7, 1), datetime(2021, 9, 30, 23, 59, 59, 999999)),
            "上季度": (datetime(2021, 4, 1), datetime(2021, 6, 30, 23, 59, 59, 999999)),
            "上个季度": (datetime(2021, 4, 1), datetime(2021, 6, 30, 23, 59, 59, 999999)),
            "下季度": (datetime(2021, 10, 1), datetime(2021, 12, 31, 23, 59, 59, 999999)),
            "下个季度": (datetime(2021, 10, 1), datetime(2021, 12, 31, 23, 59, 59, 999999)),
            "第一季度": (datetime(2021, 1, 1), datetime(2021, 3, 31, 23, 59, 59, 999999)),
            "第一个季度": (datetime(2021, 1, 1), datetime(2021, 3, 31, 23, 59, 59, 999999)),
            "第1季度": (datetime(2021, 1, 1), datetime(2021, 3, 31, 23, 59, 59, 999999)),
            "第1个季度": (datetime(2021, 1, 1), datetime(2021, 3, 31, 23, 59, 59, 999999)),
            "一季度": (datetime(2021, 1, 1), datetime(2021, 3, 31, 23, 59, 59, 999999)),
            "1季度": (datetime(2021, 1, 1), datetime(2021, 3, 31, 23, 59, 59, 999999)),
            "第二季度": (datetime(2021, 4, 1), datetime(2021, 6, 30, 23, 59, 59, 999999)),
            "第二个季度": (datetime(2021, 4, 1), datetime(2021, 6, 30, 23, 59, 59, 999999)),
            "第2季度": (datetime(2021, 4, 1), datetime(2021, 6, 30, 23, 59, 59, 999999)),
            "第2个季度": (datetime(2021, 4, 1), datetime(2021, 6, 30, 23, 59, 59, 999999)),
            "2季度": (datetime(2021, 4, 1), datetime(2021, 6, 30, 23, 59, 59, 999999)),
            "二季度": (datetime(2021, 4, 1), datetime(2021, 6, 30, 23, 59, 59, 999999)),
            "第三季度": (datetime(2021, 7, 1), datetime(2021, 9, 30, 23, 59, 59, 999999)),
            "第三个季度": (datetime(2021, 7, 1), datetime(2021, 9, 30, 23, 59, 59, 999999)),
            "第3季度": (datetime(2021, 7, 1), datetime(2021, 9, 30, 23, 59, 59, 999999)),
            "第3个季度": (datetime(2021, 7, 1), datetime(2021, 9, 30, 23, 59, 59, 999999)),
            "三季度": (datetime(2021, 7, 1), datetime(2021, 9, 30, 23, 59, 59, 999999)),
            "3季度": (datetime(2021, 7, 1), datetime(2021, 9, 30, 23, 59, 59, 999999)),
            "第四季度": (datetime(2021, 10, 1), datetime(2021, 12, 31, 23, 59, 59, 999999)),
            "第四个季度": (datetime(2021, 10, 1), datetime(2021, 12, 31, 23, 59, 59, 999999)),
            "第4季度": (datetime(2021, 10, 1), datetime(2021, 12, 31, 23, 59, 59, 999999)),
            "第4个季度": (datetime(2021, 10, 1), datetime(2021, 12, 31, 23, 59, 59, 999999)),
            "四季度": (datetime(2021, 10, 1), datetime(2021, 12, 31, 23, 59, 59, 999999)),
            "4季度": (datetime(2021, 10, 1), datetime(2021, 12, 31, 23, 59, 59, 999999)),
            "前2季度": (datetime(2021, 1, 1), datetime(2021, 6, 30, 23, 59, 59, 999999)),
            "前2个季度": (datetime(2021, 1, 1), datetime(2021, 6, 30, 23, 59, 59, 999999)),
            "前两季度": (datetime(2021, 1, 1), datetime(2021, 6, 30, 23, 59, 59, 999999)),
            "前两个季度": (datetime(2021, 1, 1), datetime(2021, 6, 30, 23, 59, 59, 999999)),
            "后2季度": (datetime(2021, 10, 1), datetime(2022, 3, 31, 23, 59, 59, 999999)),
            "后2个季度": (datetime(2021, 10, 1), datetime(2022, 3, 31, 23, 59, 59, 999999)),
            "后两季度": (datetime(2021, 10, 1), datetime(2022, 3, 31, 23, 59, 59, 999999)),
            "后两个季度": (datetime(2021, 10, 1), datetime(2022, 3, 31, 23, 59, 59, 999999)),
            "2季度前": (datetime(2021, 1, 1), datetime(2021, 3, 31, 23, 59, 59, 999999)),
            "两季度前": (datetime(2021, 1, 1), datetime(2021, 3, 31, 23, 59, 59, 999999)),
            "2季度后": (datetime(2022, 1, 1), datetime(2022, 3, 31, 23, 59, 59, 999999)),
            "两季度后": (datetime(2022, 1, 1), datetime(2022, 3, 31, 23, 59, 59, 999999)),
            "2季度内": (datetime(2021, 4, 1), datetime(2021, 9, 30, 23, 59, 59, 999999)),
            "两季度内": (datetime(2021, 4, 1), datetime(2021, 9, 30, 23, 59, 59, 999999)),
            # # 月 口语格式
            "本月": (datetime(2021, 9, 1), datetime(2021, 9, 30, 23, 59, 59, 999999)),
            "本月份": (datetime(2021, 9, 1), datetime(2021, 9, 30, 23, 59, 59, 999999)),
            "本月度": (datetime(2021, 9, 1), datetime(2021, 9, 30, 23, 59, 59, 999999)),
            "这个月": (datetime(2021, 9, 1), datetime(2021, 9, 30, 23, 59, 59, 999999)),
            "这个月份": (datetime(2021, 9, 1), datetime(2021, 9, 30, 23, 59, 59, 999999)),
            "当前月": (datetime(2021, 9, 1), datetime(2021, 9, 30, 23, 59, 59, 999999)),
            "当前月份": (datetime(2021, 9, 1), datetime(2021, 9, 30, 23, 59, 59, 999999)),
            "上月": (datetime(2021, 8, 1), datetime(2021, 8, 31, 23, 59, 59, 999999)),
            "上月份": (datetime(2021, 8, 1), datetime(2021, 8, 31, 23, 59, 59, 999999)),
            "上个月": (datetime(2021, 8, 1), datetime(2021, 8, 31, 23, 59, 59, 999999)),
            "上个月份": (datetime(2021, 8, 1), datetime(2021, 8, 31, 23, 59, 59, 999999)),
            "下月": (datetime(2021, 10, 1), datetime(2021, 10, 31, 23, 59, 59, 999999)),
            "下月份": (datetime(2021, 10, 1), datetime(2021, 10, 31, 23, 59, 59, 999999)),
            "下个月": (datetime(2021, 10, 1), datetime(2021, 10, 31, 23, 59, 59, 999999)),
            "下个月份": (datetime(2021, 10, 1), datetime(2021, 10, 31, 23, 59, 59, 999999)),
            "前2月": (datetime(2021, 7, 1), datetime(2021, 8, 31, 23, 59, 59, 999999)),
            "前2个月": (datetime(2021, 7, 1), datetime(2021, 8, 31, 23, 59, 59, 999999)),
            "前2个月份": (datetime(2021, 7, 1), datetime(2021, 8, 31, 23, 59, 59, 999999)),
            "前两月": (datetime(2021, 7, 1), datetime(2021, 8, 31, 23, 59, 59, 999999)),
            "前两个月": (datetime(2021, 7, 1), datetime(2021, 8, 31, 23, 59, 59, 999999)),
            "前两个月份": (datetime(2021, 7, 1), datetime(2021, 8, 31, 23, 59, 59, 999999)),
            "后2月": (datetime(2021, 10, 1), datetime(2021, 11, 30, 23, 59, 59, 999999)),
            "后2个月": (datetime(2021, 10, 1), datetime(2021, 11, 30, 23, 59, 59, 999999)),
            "后2个月份": (datetime(2021, 10, 1), datetime(2021, 11, 30, 23, 59, 59, 999999)),
            "后两月": (datetime(2021, 10, 1), datetime(2021, 11, 30, 23, 59, 59, 999999)),
            "后两个月": (datetime(2021, 10, 1), datetime(2021, 11, 30, 23, 59, 59, 999999)),
            "后两个月份": (datetime(2021, 10, 1), datetime(2021, 11, 30, 23, 59, 59, 999999)),
            "2月前": (datetime(2021, 7, 1), datetime(2021, 7, 31, 23, 59, 59, 999999)),
            "两月前": (datetime(2021, 7, 1), datetime(2021, 7, 31, 23, 59, 59, 999999)),
            "2月后": (datetime(2021, 11, 1), datetime(2021, 11, 30, 23, 59, 59, 999999)),
            "两月后": (datetime(2021, 11, 1), datetime(2021, 11, 30, 23, 59, 59, 999999)),
            "2月内": (datetime(2021, 8, 1), datetime(2021, 9, 30, 23, 59, 59, 999999)),
            "两月内": (datetime(2021, 8, 1), datetime(2021, 9, 30, 23, 59, 59, 999999)),
            # 周、星期 口语格式
            "本周": (datetime(2021, 8, 30), datetime(2021, 9, 5, 23, 59, 59, 999999)),
            "当前周": (datetime(2021, 8, 30), datetime(2021, 9, 5, 23, 59, 59, 999999)),
            "上周": (datetime(2021, 8, 23), datetime(2021, 8, 29, 23, 59, 59, 999999)),
            "下周": (datetime(2021, 9, 6), datetime(2021, 9, 12, 23, 59, 59, 999999)),
            "前2周": (datetime(2021, 8, 16), datetime(2021, 8, 29, 23, 59, 59, 999999)),
            "前2个周": (datetime(2021, 8, 16), datetime(2021, 8, 29, 23, 59, 59, 999999)),
            "前两周": (datetime(2021, 8, 16), datetime(2021, 8, 29, 23, 59, 59, 999999)),
            "前两个周": (datetime(2021, 8, 16), datetime(2021, 8, 29, 23, 59, 59, 999999)),
            "后2周": (datetime(2021, 9, 6), datetime(2021, 9, 19, 23, 59, 59, 999999)),
            "后2个周": (datetime(2021, 9, 6), datetime(2021, 9, 19, 23, 59, 59, 999999)),
            "后两周": (datetime(2021, 9, 6), datetime(2021, 9, 19, 23, 59, 59, 999999)),
            "后两个周": (datetime(2021, 9, 6), datetime(2021, 9, 19, 23, 59, 59, 999999)),
            "2周前": (datetime(2021, 8, 16), datetime(2021, 8, 22, 23, 59, 59, 999999)),
            "两周前": (datetime(2021, 8, 16), datetime(2021, 8, 22, 23, 59, 59, 999999)),
            "2周后": (datetime(2021, 9, 13), datetime(2021, 9, 19, 23, 59, 59, 999999)),
            "两周后": (datetime(2021, 9, 13), datetime(2021, 9, 19, 23, 59, 59, 999999)),
            "2周内": (datetime(2021, 8, 23), datetime(2021, 9, 5, 23, 59, 59, 999999)),
            "两周内": (datetime(2021, 8, 23), datetime(2021, 9, 5, 23, 59, 59, 999999)),
            "本星期": (datetime(2021, 8, 30), datetime(2021, 9, 5, 23, 59, 59, 999999)),
            "这个星期": (datetime(2021, 8, 30), datetime(2021, 9, 5, 23, 59, 59, 999999)),
            "当前星期": (datetime(2021, 8, 30), datetime(2021, 9, 5, 23, 59, 59, 999999)),
            "上星期": (datetime(2021, 8, 23), datetime(2021, 8, 29, 23, 59, 59, 999999)),
            "上个星期": (datetime(2021, 8, 23), datetime(2021, 8, 29, 23, 59, 59, 999999)),
            "下星期": (datetime(2021, 9, 6), datetime(2021, 9, 12, 23, 59, 59, 999999)),
            "下个星期": (datetime(2021, 9, 6), datetime(2021, 9, 12, 23, 59, 59, 999999)),
            "前2星期": (datetime(2021, 8, 16), datetime(2021, 8, 29, 23, 59, 59, 999999)),
            "前2个星期": (datetime(2021, 8, 16), datetime(2021, 8, 29, 23, 59, 59, 999999)),
            "前两星期": (datetime(2021, 8, 16), datetime(2021, 8, 29, 23, 59, 59, 999999)),
            "前两个星期": (datetime(2021, 8, 16), datetime(2021, 8, 29, 23, 59, 59, 999999)),
            "后2星期": (datetime(2021, 9, 6), datetime(2021, 9, 19, 23, 59, 59, 999999)),
            "后2个星期": (datetime(2021, 9, 6), datetime(2021, 9, 19, 23, 59, 59, 999999)),
            "后两星期": (datetime(2021, 9, 6), datetime(2021, 9, 19, 23, 59, 59, 999999)),
            "后两个星期": (datetime(2021, 9, 6), datetime(2021, 9, 19, 23, 59, 59, 999999)),
            "2星期前": (datetime(2021, 8, 16), datetime(2021, 8, 22, 23, 59, 59, 999999)),
            "两星期前": (datetime(2021, 8, 16), datetime(2021, 8, 22, 23, 59, 59, 999999)),
            "2星期后": (datetime(2021, 9, 13), datetime(2021, 9, 19, 23, 59, 59, 999999)),
            "两星期后": (datetime(2021, 9, 13), datetime(2021, 9, 19, 23, 59, 59, 999999)),
            "2星期内": (datetime(2021, 8, 23), datetime(2021, 9, 5, 23, 59, 59, 999999)),
            "两星期内": (datetime(2021, 8, 23), datetime(2021, 9, 5, 23, 59, 59, 999999)),
            # 日、天 口语格式
            "今日": (datetime(2021, 9, 1), datetime(2021, 9, 1, 23, 59, 59, 999999)),
            "明日": (datetime(2021, 9, 2), datetime(2021, 9, 2, 23, 59, 59, 999999)),
            "后日": (datetime(2021, 9, 3), datetime(2021, 9, 3, 23, 59, 59, 999999)),
            "昨日": (datetime(2021, 8, 31), datetime(2021, 8, 31, 23, 59, 59, 999999)),
            "前日": (datetime(2021, 8, 30), datetime(2021, 8, 30, 23, 59, 59, 999999)),
            "前2日": (datetime(2021, 8, 30), datetime(2021, 8, 31, 23, 59, 59, 999999)),
            "前2个日": (datetime(2021, 8, 30), datetime(2021, 8, 31, 23, 59, 59, 999999)),
            "前两日": (datetime(2021, 8, 30), datetime(2021, 8, 31, 23, 59, 59, 999999)),
            "前两个日": (datetime(2021, 8, 30), datetime(2021, 8, 31, 23, 59, 59, 999999)),
            "后2日": (datetime(2021, 9, 2), datetime(2021, 9, 3, 23, 59, 59, 999999)),
            "后2个日": (datetime(2021, 9, 2), datetime(2021, 9, 3, 23, 59, 59, 999999)),
            "后两日": (datetime(2021, 9, 2), datetime(2021, 9, 3, 23, 59, 59, 999999)),
            "后两个日": (datetime(2021, 9, 2), datetime(2021, 9, 3, 23, 59, 59, 999999)),
            "2日前": (datetime(2021, 8, 30), datetime(2021, 8, 30, 23, 59, 59, 999999)),
            "两日前": (datetime(2021, 8, 30), datetime(2021, 8, 30, 23, 59, 59, 999999)),
            "2日后": (datetime(2021, 9, 3), datetime(2021, 9, 3, 23, 59, 59, 999999)),
            "两日后": (datetime(2021, 9, 3), datetime(2021, 9, 3, 23, 59, 59, 999999)),
            "2日内": (datetime(2021, 8, 31), datetime(2021, 9, 1, 23, 59, 59, 999999)),
            "两日内": (datetime(2021, 8, 31), datetime(2021, 9, 1, 23, 59, 59, 999999)),
            "今天": (datetime(2021, 9, 1), datetime(2021, 9, 1, 23, 59, 59, 999999)),
            "明天": (datetime(2021, 9, 2), datetime(2021, 9, 2, 23, 59, 59, 999999)),
            "后天": (datetime(2021, 9, 3), datetime(2021, 9, 3, 23, 59, 59, 999999)),
            "昨天": (datetime(2021, 8, 31), datetime(2021, 8, 31, 23, 59, 59, 999999)),
            "前天": (datetime(2021, 8, 30), datetime(2021, 8, 30, 23, 59, 59, 999999)),
            "前2天": (datetime(2021, 8, 30), datetime(2021, 8, 31, 23, 59, 59, 999999)),
            "前2个天": (datetime(2021, 8, 30), datetime(2021, 8, 31, 23, 59, 59, 999999)),
            "前两天": (datetime(2021, 8, 30), datetime(2021, 8, 31, 23, 59, 59, 999999)),
            "前两个天": (datetime(2021, 8, 30), datetime(2021, 8, 31, 23, 59, 59, 999999)),
            "后2天": (datetime(2021, 9, 2), datetime(2021, 9, 3, 23, 59, 59, 999999)),
            "后2个天": (datetime(2021, 9, 2), datetime(2021, 9, 3, 23, 59, 59, 999999)),
            "后两天": (datetime(2021, 9, 2), datetime(2021, 9, 3, 23, 59, 59, 999999)),
            "后两个天": (datetime(2021, 9, 2), datetime(2021, 9, 3, 23, 59, 59, 999999)),
            "2天前": (datetime(2021, 8, 30), datetime(2021, 8, 30, 23, 59, 59, 999999)),
            "两天前": (datetime(2021, 8, 30), datetime(2021, 8, 30, 23, 59, 59, 999999)),
            "2天后": (datetime(2021, 9, 3), datetime(2021, 9, 3, 23, 59, 59, 999999)),
            "两天后": (datetime(2021, 9, 3), datetime(2021, 9, 3, 23, 59, 59, 999999)),
            "2天内": (datetime(2021, 8, 31), datetime(2021, 9, 1, 23, 59, 59, 999999)),
            "两天内": (datetime(2021, 8, 31), datetime(2021, 9, 1, 23, 59, 59, 999999)),
            "上午": (datetime(2021, 9, 1), datetime(2021, 9, 1, 11, 59, 59, 999999)),
            "下午": (datetime(2021, 9, 1, 12), datetime(2021, 9, 1, 18, 59, 59, 999999)),
        }

    def test_cn2date(self):
        for text, expected in self.norm_data_dict.items():
            result = parse(text)
            assert len(result) == len(expected)

            for i, d in enumerate(expected):
                r = result[i].datetime()
                assert r.year == d.year
                assert r.month == d.month
                assert r.day == d.day
                assert r.hour == d.hour
                assert r.minute == d.minute
                assert r.second == d.second
                assert r.microsecond == d.microsecond

        for text, expected in self.cn_data_dict.items():
            result = parse(text)
            assert len(result) == len(expected)

            for i, d in enumerate(expected):
                r = result[i].datetime()
                assert r.year == d.year
                assert r.month == d.month
                assert r.day == d.day
                assert r.hour == d.hour
                assert r.minute == d.minute
                assert r.second == d.second
                assert r.microsecond == d.microsecond


if __name__ == "__main__":
    unittest.main()
