from __future__ import annotations

from pathlib import Path

default_filename = "date.lark"


def get_default_conf() -> list[str]:
    file = Path(__file__).parent / default_filename
    conf_content = open(file, "r", encoding="utf-8").read()
    return conf_content.split("===")
