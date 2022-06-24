# pyright: strict

from __future__ import annotations

from datetime import datetime

from cn2date.s2e import S2E
from cn2date.transform import TransformerBase, TransformInfo


class Cn2Date:
    __extensions: list[TransformerBase] = []

    def get_extensions(self) -> tuple[TransformerBase]:
        return tuple(self.__extensions)

    def add_extensions(self, *extensions: TransformerBase) -> Cn2Date:
        for extension in extensions:
            self.__extensions.append(extension)
        return self

    def remove_extensions(self, *extensions: TransformerBase) -> Cn2Date:
        for extension in extensions:
            self.__extensions.remove(extension)
        return self

    def parse(self, text: str) -> tuple[datetime, datetime]:
        if text is None or text.isspace():
            raise ValueError("The parameter text is None or empty")

        if not any(self.__extensions):
            raise IndexError("No extension is added")

        transform_info = TransformInfo().initialize(text)
        return self.__preceded(transform_info).to_tuple()

    def __preceded(self, transform_info: TransformInfo) -> S2E:
        for ext in self.__extensions:
            if ext.initialize(transform_info).transform():
                if transform_info.result is None:
                    raise ValueError(f"Can't parse the text: {transform_info.original_input}")
                return transform_info.result

        raise ValueError(f"No extension could handle the text: {transform_info.original_input}")
