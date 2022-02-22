import sys
from pathlib import Path

proj_dir = Path(__file__).parent.parent

sys.path.append(str(proj_dir))

from cn2date import parse

words = ["2021-9-17", "2021年9月17日", "二零二一年九月十七日", "今天", "本季度", "2020年上半年"]

for word in words:
    print(parse(word))
