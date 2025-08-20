from ..core.proto import ExtractionResult
from ..core.base_extractor import BaseExtractor


CHINESE_MAPPINGS = {"本": "当前,这个,这", "内": "以内,之内", "以前": "之前"}
YEAR_MAPPINGS = {"今": "本", "去年": "上年", "明年": "下年"}
QUARTER_MAPPINGS = {"上": "上个", "下": "下个"}
MONTH_MAPPINGS = {"上": "上个", "下": "下个"}
WEEK_MAPPINGS = {"周": "星期", "上": "上个", "下": "下个"}
DAY_MAPPINGS = {"天": "日"}


STANDARDIZED_DATE_FORMAT_GRAMMAR = """
start: date

date  : years _year_delimiter months _month_delimiter days _day_delimiter? | years _year_delimiter months _month_delimiter? | months _month_delimiter days _day_delimiter? | years _year_delimiter? | months _month_delimiter? | days _day_delimiter?
years : ZERO_NINE ZERO_NINE | ONE_NINE ZERO_NINE ZERO_NINE ZERO_NINE
months: ONE_NINE | /[0零]/ ONE_NINE | /[1一]/ /[0-2零一二]/ | /十/ /[12一二]/?
days  : ONE_NINE | /[0零]/ ONE_NINE | /[12一二]/ ZERO_NINE | /[2二]/? /十/ | /[2二]/? /十/ ONE_NINE | /[3三]/ (/[01零一]/ | /十/ /[1一]/?)

_year_delimiter : "年" | _std_delimiter
_month_delimiter: "月" | _std_delimiter
_day_delimiter  : "日" | "号"
_std_delimiter  : "-" | "/"

ZERO_NINE: /[0-9零一二三四五六七八九]/
ONE_NINE : /[1-9一二三四五六七八九]/
"""
"""标准化日期格式解析规则语法"""


CHINESE_UNSTRUCTURED_TEXT_GRAMMAR = """
start: date

date     : years | quarters | months | days | weeks | long_time
years    : FIRST YEAR_UNIT | FIRST? _digit "个"? YEAR_UNIT ADVERB?
quarters : FIRST QUARTER_UNIT | FIRST? _digit "个"? QUARTER_UNIT ADVERB?
months   : FIRST MONTH_UNIT | FIRST? _digit "个"? MONTH_UNIT ADVERB?
weeks    : FIRST WEEK_UNIT | FIRST? _digit "个"? WEEK_UNIT ADVERB?
days     : FIRST DAY_UNIT | FIRST? _digit "个"? DAY_UNIT ADVERB?
long_time: FIRST LONG_TIME_UNIT | FIRST? _digit LONG_TIME_UNIT ADVERB?

_digit: DIGIT | CHINE_DIGIT

FIRST         : "今" | "本" | "当前" | "这个" | "明" | "昨" | "去" | "前" | "后" | "上半" | "下半" | "上" | "上个" | "下" | "下个"
ADVERB        : "以来" | "以前" | "以后" | "之前" | "之后" | "前" | "后" | "内" | "以内" | "之内"
YEAR_UNIT     : "年"
QUARTER_UNIT  : "季度"
MONTH_UNIT    : "月"
WEEK_UNIT     : "周" | "星期"
DAY_UNIT      : "天" | "日"
LONG_TIME_UNIT: "午"
CHINE_DIGIT   : "两"
DIGIT         : /["0-9零一二三四五六七八九十"]/

%ignore " " | "份" | "度" | "第"
"""
"""中文非结构化文本日期格式解析规则语法"""


class RuleBasedExtractor(BaseExtractor):
    def extract(self, text: str) -> ExtractionResult: ...

    @property
    def name(self) -> str:
        return "rule_based_extractor"
