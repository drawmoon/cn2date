import sys
from pathlib import Path

from freezegun import freeze_time

proj_dir = Path(__file__).parent.parent

sys.path.append(str(proj_dir))

from cn2date import parse


@freeze_time("2021-9-1 11:23:45")
def main():
    words = [
        "2023年",
        "二零二三年十二月二十一日",
        "今年",
        "本季度",
    ]

    for word in words:
        between = parse(word)
        print(f"{word}:")
        between.output()
        print("-" * 50)


if __name__ == "__main__":
    main()
