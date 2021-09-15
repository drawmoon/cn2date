import hanlp

from typing import List, Tuple


han_lp = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)

# 设置白名单
dic = {"1季度": "DATE", "第1季度": "DATE", "第1个季度": "DATE", "一季度": "DATE",
       "2季度": "DATE", "第2季度": "DATE", "第2个季度": "DATE", "二季度": "DATE",
       "3季度": "DATE", "第3季度": "DATE", "第3个季度": "DATE", "三季度": "DATE",
       "4季度": "DATE", "第4季度": "DATE", "第4个季度": "DATE", "四季度": "DATE",
       "这个季度": "DATE"}
han_lp["ner/ontonotes"].dict_whitelist = dict([(k, v) for k, v in dic.items() if v == "DATE"])


def merge(lst: List[Tuple[str, str, int, int]]):
    merged = []
    slice_word = ""
    slice_s = 0
    for i, (word, typ, s, e) in enumerate(lst):
        if slice_word == "":
            slice_s = s
        nxt = lst[i + 1] if len(lst) > i + 1 else None
        # 如果没有相邻的或已经是最后一个元素
        if nxt is None or e != nxt[2]:
            if slice_word != "":
                merged.append((slice_word + word, typ, slice_s, e))
                slice_word = ""
            else:
                merged.append((word, typ, s, e))
        else:
            # 下一个元素的类型与当前的类型一致，需要合并
            if typ == nxt[1]:
                slice_word += word
            # 当前的类型是序数、整数或基数并且下一个元素的类型是日期或时间，需要合并
            elif typ in ["ORDINAL", "INTEGER", "CARDINAL"] and nxt[1] in ["DATE", "TIME"]:
                slice_word += word
    return merged
