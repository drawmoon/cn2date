from cn2date import parse

from util import han_lp, merge


def process_input(text):
    print("输入的字符:", text)

    doc = han_lp(text)
    ner = merge(doc["ner/ontonotes"])

    dt_text = ner[0][0]
    print("查找到的日期:", dt_text)
    return dt_text


input_text = "第四季度总共有多少订单"

word = process_input(input_text)
print("结果:", parse(word))
