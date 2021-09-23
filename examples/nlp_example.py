from cn2date.cn2date import Cn2Date

from util import han_lp, merge


parse = Cn2Date().parse


def process_input(text):
    print("输入的字符:", text)

    doc = han_lp(text)
    ner = merge(doc["ner/ontonotes"])

    dt_text = ner[0][0]
    print("查找到的日期:", dt_text)
    return dt_text


input_text = "第四季度总共有多少订单"

input_date = process_input(input_text)
result = parse(input_date)
print("解析为查询条件:", end="")
if None in result:
    if result[0] is None:
        print(f"时间 < '{result[1]}'")
    else:
        print(f"时间 >= '{result[0]}'")
else:
    print(f"时间 >= '{result[0]}' and 时间 < '{result[1]}'")
