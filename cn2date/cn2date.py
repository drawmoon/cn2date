from datetime import datetime
from typing import List, Tuple

from cn2date.s2e import S2E
from cn2date.source import last
from cn2date.transform import ITransformer


class Cn2Date:
    __exts: List[ITransformer] = []

    def get_ext(self) -> Tuple[ITransformer]:
        return tuple(self.__exts)

    def add_ext(self, ext: ITransformer):
        self.__exts.append(ext)
        
        return self

    def remove_ext(self, ext: ITransformer):
        self.__exts.remove(ext)

        return self

    def parse(self, text: str) -> Tuple[datetime, datetime]:
        if text is None or text.isspace():
            raise ValueError("The parameter text is None or empty")

        if not any(self.__exts):
            raise ValueError("No extension is added")

        return self.__preceded(text).to_tuple()

    def __preceded(self, text: str) -> S2E:
        for ext in self.__exts:
            source = ext.transform(text)
            s2e = last(source)
            
            if s2e is not None:
                return s2e
        
        raise ValueError(f"Can't parse the text: {text}")
