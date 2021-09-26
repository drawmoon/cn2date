from pyinstrument import Profiler

from cn2date.cn2date import Cn2Date


profiler = Profiler()
profiler.start()

parse = Cn2Date().parse

words = [
    "2021-9-17",
    "2021年9月17日",
    "二零二一年九月十七日",
    "今天",
    "2020年上半年",
    "本季度"
]

for word in words:
    print(parse(word))

profiler.stop()

profiler.print()
