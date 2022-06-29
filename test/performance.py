import sys
from pathlib import Path

proj_dir = Path(__file__).parent.parent

sys.path.append(str(proj_dir))

from pyinstrument import Profiler

words = ["2021-9-17", "2021年9月17日", "二零二一年九月十七日", "今年", "本季度", "今天"]


def main(text: str):
    p = Profiler()
    with p:
        from cn2date import parse

        print(f"Input text: {text}, parse result: {parse(text)}")
    p.print()


for word in words:
    main(word)
