from cn2date.transform import DateTransformer

from .cn2date import Cn2Date

__version__ = "0.0.5-beta1"


def create_default() -> Cn2Date:
    return Cn2Date().add_extensions(DateTransformer())


default = create_default()
parse = default.parse
