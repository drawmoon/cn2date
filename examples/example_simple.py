from cn2date.cn2date import parse


words = [
    "2021-9-17",
    "2021年9月17日",
    "二零二一年九月十七日",
    "今天",
    "2020年上半年",
    "本季度"
]

for word in words:
    result = parse(word)
    print(result)
