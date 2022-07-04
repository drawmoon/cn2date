from cn2date.transform import DateTransformer, NLTransformer

from .cn2date import Cn2Date

__title__ = "cn2date"
__description__ = "中文日期 、口语 转换为 日期字符串"
__version__ = "0.1.0b1"


def create_default() -> Cn2Date:
    return Cn2Date().add_extensions(DateTransformer(), NLTransformer())


default = create_default()
parse = default.parse

__all__ = [
    "__title__",
    "__description__",
    "__version__",
    "parse",
    "default",
    "create_default",
]
