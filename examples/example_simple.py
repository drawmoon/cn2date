import sys
from pathlib import Path

proj_dir = Path(__file__).parent.parent

sys.path.append(str(proj_dir))

from cn2date import parse

words = ["2021年", "二零二一年九月十七日", "今年", "本季度", "今天"]

for word in words:
    print(parse(word))
