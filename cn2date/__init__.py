from cn2date.__version__ import __description__, __title__, __version__
from cn2date.transform import DateTransformer, NLTransformer

from .cn2date import Cn2Date

__all__ = [
    "__title__",
    "__description__",
    "__version__",
    "parse",
    "default",
    "create_default",
]


def create_default() -> Cn2Date:
    return Cn2Date().add_extensions(DateTransformer(), NLTransformer())


default = create_default()
parse = default.parse
