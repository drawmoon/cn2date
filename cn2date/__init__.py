# pyright: strict

from __future__ import annotations

from datetime import datetime
from typing import Callable

from cn2date.transform import DateTransformer, NLTransformer

from .cn2date import Cn2Date

__title__: str = "cn2date"
__description__: str = "中文日期 、口语 转换为 日期字符串"
__version__: str = "0.1.0b2"


def create_default() -> Cn2Date:
    return Cn2Date().add_extensions(DateTransformer(), NLTransformer())


default: Cn2Date = create_default()
parse: Callable[[str], tuple[datetime, datetime]] = default.parse

__all__: list[str] = [
    "__title__",
    "__description__",
    "__version__",
    "parse",
    "default",
    "create_default",
]
