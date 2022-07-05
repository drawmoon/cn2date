# pyright: strict

from __future__ import annotations

from datetime import datetime

from typing_extensions import Literal

from cn2date.s2e import S2E


class TransformInfo:
    """ """

    input: str
    current: str
    args: list[int]
    result: S2E | None
    errs: list[str]
    intent: Literal["date", "nl", "group"] | str | None

    def initialize(self, text: str) -> TransformInfo:
        """

        :param text:
        :return:
        """
        self.input = text
        self.current = ""
        self.args = []
        self.result = None
        self.errs = []
        self.intent = None

        return self

    def write(self, start: datetime, end: datetime) -> None:
        """

        :param start:
        :param end:
        :return:
        """
        self.result = S2E(start, end)
        self.current = ""
