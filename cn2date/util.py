import cn2an

from typing import Optional, List, Union
from datetime import datetime
from dateutil.relativedelta import relativedelta


def now() -> datetime:
    # 方便进行单元测试
    return datetime(2021, 9, 1)


def str2digit(s: str, typ: Optional[str] = None) -> int:
    opt = cn2an.transform(s)
    if not opt.isdigit():
        raise TypeError("字符转换为数字失败")
    if typ == "year":
        if len(opt) == 2:
            opt = str(now().year)[0:2] + opt
    return int(opt)


def build_date(year: int, month: Optional[int] = None, day: Optional[int] = None) -> Union[List[datetime], None]:
    # 处理 年月日
    if year is not None and month is not None and day is not None:
        start_date = datetime(year, month, day)
        end_date = start_date + relativedelta(days=1)
        return [start_date, end_date]

    # 处理 年月
    if year is not None and month is not None:
        start_date = datetime(year, month, 1)
        end_date = start_date + relativedelta(months=1)
        return [start_date, end_date]

    # 处理 年
    if year is not None:
        start_date = datetime(year, 1, 1)
        end_date = start_date + relativedelta(years=1)
        return [start_date, end_date]

    return None


def date_format(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")
